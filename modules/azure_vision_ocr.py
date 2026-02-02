"""
Azure OpenAI Vision OCR Module
High-performance OCR using GPT-4o Vision with parallel processing and caching
"""
import base64
import io
import hashlib
import shelve
import gc
from pathlib import Path
from typing import Optional, List, Tuple
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from openai import AzureOpenAI
from PIL import Image, ImageEnhance, ImageFilter
from config import Config

# PDF library check
try:
    import fitz  # PyMuPDF
    PDF_SUPPORT = True
except ImportError:
    PDF_SUPPORT = False
    print("⚠️ PyMuPDF not installed. PDF OCR will not be available.")


class AzureVisionOCR:
    """Azure OpenAI Vision OCR with parallel processing and smart caching"""
    
    def __init__(self):
        """Initialize Azure Vision OCR client and cache"""
        self.client = AzureOpenAI(
            api_key=Config.AZURE_OPENAI_KEY,
            api_version=Config.AZURE_OPENAI_API_VERSION,  # Use config value
            azure_endpoint=Config.AZURE_OPENAI_ENDPOINT
        )
        self.deployment = Config.AZURE_OPENAI_DEPLOYMENT
        
        # Cache setup
        self.cache_dir = Path.home() / ".brd_ocr_cache"
        self.cache_dir.mkdir(exist_ok=True)
        self.cache_enabled = True
        
        # Performance settings
        self.max_workers = 3  # Parallel threads (respects Azure rate limits)
        self.dpi = 250  # Balanced quality/speed
    
    def _get_cache_key(self, file_path: str, page_num: int) -> str:
        """Generate cache key from file path, modified time, and page number"""
        file_stat = Path(file_path).stat()
        cache_string = f"{file_path}_{file_stat.st_mtime}_{file_stat.st_size}_{page_num}"
        return hashlib.md5(cache_string.encode()).hexdigest()
    
    def _get_cached_result(self, cache_key: str) -> Optional[str]:
        """Retrieve cached OCR result if available"""
        if not self.cache_enabled:
            return None
        
        try:
            cache_file = self.cache_dir / "ocr_cache"
            with shelve.open(str(cache_file)) as cache:
                if cache_key in cache:
                    print(f"  💾 Cache hit!")
                    return cache[cache_key]
        except Exception as e:
            print(f"  ⚠️ Cache read error: {e}")
        
        return None
    
    def _save_to_cache(self, cache_key: str, result: str):
        """Save OCR result to persistent cache"""
        if not self.cache_enabled:
            return
        
        try:
            cache_file = self.cache_dir / "ocr_cache"
            with shelve.open(str(cache_file)) as cache:
                cache[cache_key] = result
        except Exception as e:
            print(f"  ⚠️ Cache write error: {e}")
    
    def _preprocess_image(self, img: Image.Image) -> Image.Image:
        """Enhance image for better OCR accuracy"""
        # Auto-crop whitespace
        bbox = img.getbbox()
        if bbox:
            img = img.crop(bbox)
        
        # Enhance contrast for better text visibility
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(1.2)
        
        # Slight sharpening for text clarity
        img = img.filter(ImageFilter.SHARPEN)
        
        return img
    
    def _detect_page_content_type(self, img: Image.Image) -> str:
        """Detect if page is text-heavy or image-heavy"""
        # Simple heuristic: check color variation
        # Text pages typically have less color variation
        extrema = img.convert('L').getextrema()
        variation = extrema[1] - extrema[0]
        
        return "text" if variation < 200 else "image"
    
    def _encode_image_optimized(self, img: Image.Image, content_type: str = "text") -> Tuple[bytes, str]:
        """Encode image with adaptive compression based on content"""
        buffer = io.BytesIO()
        
        if content_type == "text":
            # PNG for text-heavy pages (lossless)
            img.save(buffer, format='PNG', optimize=True)
            mime_type = "image/png"
        else:
            # JPEG for image-heavy pages (smaller size)
            img.save(buffer, format='JPEG', quality=90, optimize=True)
            mime_type = "image/jpeg"
        
        buffer.seek(0)
        image_data = buffer.getvalue()
        return image_data, mime_type
    
    def _extract_page_with_cache(self, pdf_document, page_num: int, total_pages: int, 
                                  file_path: str, debug: bool = False, debug_dir: Path = None) -> str:
        """Extract text from a single PDF page with caching"""
        cache_key = self._get_cache_key(file_path, page_num)
        
        # Check cache first
        cached_result = self._get_cached_result(cache_key)
        if cached_result:
            return cached_result
        
        print(f"🔍 Processing page {page_num + 1}/{total_pages} with Azure Vision OCR...")
        
        try:
            # Get the page
            page = pdf_document[page_num]
            
            # Render page to image
            mat = fitz.Matrix(self.dpi/72, self.dpi/72)
            pix = page.get_pixmap(matrix=mat, alpha=False)
            
            # Convert to PIL Image
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            
            # Clear pixmap to free memory
            pix = None
            gc.collect()
            
            # Preprocess image for better accuracy
            img = self._preprocess_image(img)
            
            # Save debug image if requested
            if debug and debug_dir:
                debug_path = debug_dir / f"page_{page_num + 1}.png"
                img.save(debug_path, format='PNG')
                print(f"  💾 Saved debug image: {debug_path}")
            
            # Detect content type and encode accordingly
            content_type = self._detect_page_content_type(img)
            image_data, mime_type = self._encode_image_optimized(img, content_type)
            base64_image = base64.b64encode(image_data).decode('utf-8')
            
            print(f"  📤 Image: {len(image_data) / 1024:.1f} KB ({content_type} page, {mime_type})")
            
            # Extract text using Azure OpenAI Vision
            try:
                response = self.client.chat.completions.create(
                    model=self.deployment,
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "text",
                                    "text": f"Extract all text from page {page_num + 1} of this business requirements document. Include tables, requirements, and technical specifications."
                                },
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:{mime_type};base64,{base64_image}"
                                    }
                                }
                            ]
                        }
                    ],
                    temperature=0.0,
                    max_tokens=8000
                )
                
                page_text = response.choices[0].message.content.strip()
                
                # Validate and clean response
                invalid_starts = [
                    "here is", "the text", "this document", "this page",
                    "i can see", "the image", "this is", "based on",
                    "extracted text", "the content", "from the"
                ]
                
                if any(page_text.lower().startswith(start) for start in invalid_starts):
                    print(f"  ⚠️ Detected commentary, extracting pure text...")
                    lines = page_text.split('\n')
                    page_text = '\n'.join(lines[1:]) if len(lines) > 1 else page_text
                
                print(f"  ✅ Page {page_num + 1}: Extracted {len(page_text)} characters")
                print(f"  📝 Preview: {page_text[:100]}...")
                
                # Save to cache
                self._save_to_cache(cache_key, page_text)
                
                return page_text
                
            except Exception as e:
                error_msg = f"Failed to OCR page {page_num + 1}: {str(e)}"
                print(f"  ❌ {error_msg}")
                return f"--- Page {page_num + 1} ---\n[OCR failed - {str(e)}]"
                
        except Exception as e:
            error_msg = f"Page rendering error: {str(e)}"
            print(f"  ❌ {error_msg}")
            return f"--- Page {page_num + 1} ---\n[Rendering failed]"
    
    def extract_text_from_image(self, image_path: str) -> str:
        """Extract text from a single image file"""
        try:
            with Image.open(image_path) as img:
                # Convert to RGB if necessary
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Preprocess
                img = self._preprocess_image(img)
                
                # Detect content and encode
                content_type = self._detect_page_content_type(img)
                image_data, mime_type = self._encode_image_optimized(img, content_type)
                base64_image = base64.b64encode(image_data).decode('utf-8')
                
                # Call Azure OpenAI Vision API
                response = self.client.chat.completions.create(
                    model=self.deployment,
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "text",
                                    "text": "Extract all text from this image. Include tables and formatted content."
                                },
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:{mime_type};base64,{base64_image}"
                                    }
                                }
                            ]
                        }
                    ],
                    temperature=0.0,
                    max_tokens=8000
                )
                
                text = response.choices[0].message.content
                return text.strip()
                
        except Exception as e:
            return f"Error extracting text from image: {str(e)}"
    
    def extract_text_from_pdf_pages(self, pdf_path: str, debug: bool = False) -> str:
        """
        Extract text from all pages of a PDF using parallel processing
        
        Args:
            pdf_path: Path to PDF file
            debug: Save intermediate images for debugging
            
        Returns:
            Extracted text from all pages
        """
        if not PDF_SUPPORT:
            return "⚠️ PyMuPDF not installed. Run: pip install PyMuPDF"
        
        try:
            print("📄 Processing PDF with parallel Azure Vision OCR...")
            
            # Open PDF
            pdf_document = fitz.open(pdf_path)
            total_pages = len(pdf_document)
            
            # Setup debug directory if needed
            debug_dir = None
            if debug:
                debug_dir = Path(pdf_path).parent / "ocr_debug"
                debug_dir.mkdir(exist_ok=True)
                print(f"🐛 Debug mode: Images saved to {debug_dir}")
            
            # Parallel processing of pages
            page_results = {}
            
            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                # Submit all pages for processing
                future_to_page = {
                    executor.submit(
                        self._extract_page_with_cache,
                        pdf_document, page_num, total_pages, pdf_path, debug, debug_dir
                    ): page_num
                    for page_num in range(total_pages)
                }
                
                # Collect results as they complete
                for future in as_completed(future_to_page):
                    page_num = future_to_page[future]
                    try:
                        page_text = future.result()
                        page_results[page_num] = f"--- Page {page_num + 1} ---\n{page_text}"
                    except Exception as e:
                        print(f"  ❌ Page {page_num + 1} failed: {e}")
                        page_results[page_num] = f"--- Page {page_num + 1} ---\n[Error: {str(e)}]"
            
            # Close PDF
            pdf_document.close()
            
            # Combine results in page order
            all_text = [page_results[i] for i in sorted(page_results.keys())]
            result = "\n\n".join(all_text)
            
            print(f"✅ Parallel OCR completed: {len(result)} chars from {total_pages} pages")
            
            if debug and debug_dir:
                text_path = debug_dir / "extracted_text.txt"
                with open(text_path, 'w', encoding='utf-8') as f:
                    f.write(result)
                print(f"💾 Saved extracted text to: {text_path}")
            
            return result
            
        except Exception as e:
            error_msg = f"Error processing PDF: {str(e)}"
            print(error_msg)
            return error_msg
