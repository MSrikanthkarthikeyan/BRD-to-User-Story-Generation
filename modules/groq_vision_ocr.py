"""
Groq Vision OCR - Free, unlimited OCR using Groq Vision models
No installation required - uses existing Groq API key
Pure Python - no external dependencies needed!
"""
import base64
import io
from pathlib import Path
from groq import Groq
from config import Config

# Use PyMuPDF (fitz) instead of pdf2image - no poppler required!
try:
    import fitz  # PyMuPDF
    from PIL import Image
    PDF_SUPPORT = True
except ImportError:
    PDF_SUPPORT = False

class GroqVisionOCR:
    """OCR using Groq's vision models"""
    
    def __init__(self):
        self.client = Groq(api_key=Config.GROQ_API_KEY)
        # Try latest Llama 4 Scout vision model, fallback to 11b if unavailable
        # Meta Llama 4 Scout supports multimodal (text + image) inputs
        self.vision_model = "meta-llama/llama-4-scout-17b-16e-instruct"
        self.fallback_model = "llama-3.2-11b-vision-preview"
    
    def extract_text_from_image(self, image_path: str) -> str:
        """
        Extract text from a single image using Groq Vision
        
        Args:
            image_path: Path to image file
            
        Returns:
            Extracted text
        """
        try:
            # Read and encode image
            with open(image_path, 'rb') as img_file:
                image_data = img_file.read()
            
            base64_image = base64.b64encode(image_data).decode('utf-8')
            
            # Determine image type
            ext = Path(image_path).suffix.lower()
            mime_type = {
                '.png': 'image/png',
                '.jpg': 'image/jpeg',
                '.jpeg': 'image/jpeg',
                '.gif': 'image/gif',
                '.webp': 'image/webp'
            }.get(ext, 'image/jpeg')
            
            # Call Groq Vision API with enhanced prompt
            response = self.client.chat.completions.create(
                model=self.vision_model,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": """You are performing OCR (Optical Character Recognition) on this document image.

CRITICAL INSTRUCTIONS:
1. Extract EVERY word, number, symbol, and character visible in the image
2. Maintain the EXACT original layout, spacing, and structure
3. Preserve headers, titles, section numbers, bullet points, and formatting
4. If there are tables, preserve their structure using spaces or tabs
5. If there are multiple columns, extract left-to-right, top-to-bottom
6. Include page numbers, headers, footers if present
7. Do NOT add any commentary, explanations, or descriptions
8. Do NOT interpret or summarize - extract verbatim
9. If text is unclear, make your best attempt
10. Return ONLY the extracted text

Extract the text now:"""
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
                temperature=0.0,  # Zero temperature for maximum accuracy
                max_tokens=8000  # Increased for large documents
            )
            
            text = response.choices[0].message.content
            return text.strip()
            
        except Exception as e:
            print(f"Groq Vision OCR error: {e}")
            return f"Error extracting text: {str(e)}"
    
    def extract_text_from_pdf_pages(self, pdf_path: str, debug=False) -> str:
        """
        Extract text from PDF using PyMuPDF and Groq Vision
        Zero external dependencies - pure Python!
        
        Args:
            pdf_path: Path to PDF file
            debug: If True, save rendered images for debugging
            
        Returns:
            Extracted text from all pages
        """
        if not PDF_SUPPORT:
            return "⚠️ PyMuPDF not installed. Run: pip install PyMuPDF"
        
        try:
            print("📄 Converting PDF pages to images with PyMuPDF (no poppler needed)...")
            
            # Open PDF with PyMuPDF
            pdf_document = fitz.open(pdf_path)
            total_pages = len(pdf_document)
            
            # Create debug directory if needed
            if debug:
                debug_dir = Path(pdf_path).parent / "ocr_debug"
                debug_dir.mkdir(exist_ok=True)
                print(f"🐛 Debug mode: Images will be saved to {debug_dir}")
            
            all_text = []
            
            for page_num in range(total_pages):
                print(f"🔍 Processing page {page_num + 1}/{total_pages} with Groq Vision OCR...")
                
                # Get the page
                page = pdf_document[page_num]
                
                # Render page to image (pixmap)
                # Use 300 DPI for maximum quality (increased from 200)
                mat = fitz.Matrix(300/72, 300/72)
                pix = page.get_pixmap(matrix=mat, alpha=False)
                
                # Convert pixmap to PIL Image
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                
                # Save debug image if requested
                if debug:
                    debug_path = debug_dir / f"page_{page_num + 1}.png"
                    img.save(debug_path, format='PNG')
                    print(f"  💾 Saved debug image: {debug_path}")
                
                # Convert to base64
                buffer = io.BytesIO()
                img.save(buffer, format='PNG', optimize=False, quality=100)
                buffer.seek(0)
                image_data = buffer.getvalue()
                base64_image = base64.b64encode(image_data).decode('utf-8')
                
                print(f"  📤 Image size: {len(image_data) / 1024:.1f} KB, Base64: {len(base64_image)} chars")
                
                # Extract text using Groq Vision with STRICT anti-hallucination prompt
                try:
                    response = self.client.chat.completions.create(
                        model=self.vision_model,
                        messages=[
                            {
                                "role": "system",
                                "content": "You are an OCR system. Your ONLY job is to transcribe visible text from images. Never generate, invent, or hallucinate text. If no text is visible, return 'NO TEXT VISIBLE'."
                            },
                            {
                                "role": "user",
                                "content": [
                                    {
                                        "type": "text",
                                        "text": f"""STRICT OCR TASK - Page {page_num + 1}:

DO NOT CREATE OR INVENT ANY TEXT. ONLY transcribe what you SEE.

RULES:
1. Transcribe EXACTLY what text is visible in the image
2. If you cannot see clear text, say "NO TEXT VISIBLE"  
3. Do NOT make up content, summarize, or describe the image
4. Do NOT add introductions like "Here is the text" or "The document contains"
5. Start transcribing immediately - first word should be from the document
6. Preserve layout: indentation, line breaks, spacing
7. Include headers, footers, page numbers if visible
8. If image is blurry/unclear, transcribe what you can read

START TRANSCRIPTION (first word must be from the actual document):"""
                                    },
                                    {
                                        "type": "image_url",
                                        "image_url": {
                                            "url": f"data:image/png;base64,{base64_image}"
                                        }
                                    }
                                ]
                            }
                        ],
                        temperature=0.0,  # Zero temperature - no creativity
                        max_tokens=8000,
                        top_p=0.1  # Very focused sampling
                    )
                    
                    page_text = response.choices[0].message.content.strip()
                    
                    # Validate the response isn't commentary or hallucination
                    invalid_starts = [
                        "here is", "the text", "this document", "this page", 
                        "i can see", "the image", "this is", "based on",
                        "the visible text", "transcription:", "text content:"
                    ]
                    
                    # Check if response starts with commentary
                    first_line = page_text.split('\n')[0].lower() if page_text else ""
                    if any(first_line.startswith(phrase) for phrase in invalid_starts):
                        print(f"  ⚠️ Detected commentary, attempting to extract pure text...")
                        # Try to extract actual content after commentary
                        lines = page_text.split('\n')
                        # Skip commentary lines
                        actual_content = []
                        found_content = False
                        for line in lines:
                            line_lower = line.lower()
                            # Skip obvious commentary
                            if not found_content and any(phrase in line_lower for phrase in invalid_starts):
                                continue
                            # Once we find content, keep everything
                            if line.strip():
                                found_content = True
                                actual_content.append(line)
                        
                        if actual_content:
                            page_text = '\n'.join(actual_content)
                    
                    # Check if it said no text visible
                    if "NO TEXT VISIBLE" in page_text.upper() or len(page_text) < 10:
                        print(f"  ⚠️ Page {page_num + 1}: Minimal or no text detected")
                        all_text.append(f"--- Page {page_num + 1} ---\n[Minimal text or image-only page]")
                    else:
                        all_text.append(f"--- Page {page_num + 1} (Groq Vision OCR) ---\n{page_text}")
                        print(f"  ✅ Page {page_num + 1}: Extracted {len(page_text)} characters")
                        # Show first 100 chars for verification
                        preview = page_text[:100].replace('\n', ' ')
                        print(f"  📝 Preview: {preview}...")
                    
                except Exception as e:
                    error_msg = f"Failed to OCR page {page_num + 1}: {str(e)}"
                    print(f"  ❌ {error_msg}")
                    all_text.append(f"--- Page {page_num + 1} ---\n[OCR Error: {str(e)}]")
            
            # Close PDF
            pdf_document.close()
            
            result = "\n\n".join(all_text)
            print(f"✅ Groq Vision OCR completed: Extracted {len(result)} characters from {total_pages} pages")
            
            if debug:
                # Save extracted text for review
                text_path = debug_dir / "extracted_text.txt"
                with open(text_path, 'w', encoding='utf-8') as f:
                    f.write(result)
                print(f"💾 Saved extracted text to: {text_path}")
            
            return result
            
        except Exception as e:
            error_msg = f"Error processing PDF with PyMuPDF: {str(e)}"
            print(error_msg)
            return error_msg

