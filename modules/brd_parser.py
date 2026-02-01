"""
Task 1: BRD Parsing Module
Analyzes uploaded BRD documents for structure and completeness
"""
import PyPDF2
import docx
from pathlib import Path
from modules.llm_service import LLMService

# OCR imports
try:
    import pytesseract
    from pdf2image import convert_from_path
    from PIL import Image
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False

class BRDParser:
    """Parse and analyze Business Requirement Documents"""
    
    def __init__(self):
        self.llm_service = LLMService()
        
        # Try to set Tesseract path for Windows
        if OCR_AVAILABLE:
            try:
                # Common Windows installation paths
                import os
                possible_paths = [
                    r"C:\Program Files\Tesseract-OCR\tesseract.exe",
                    r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
                ]
                for path in possible_paths:
                    if os.path.exists(path):
                        pytesseract.pytesseract.tesseract_cmd = path
                        break
            except:
                pass
    
    def extract_text_from_file(self, file_path: str) -> str:
        """
        Extract text content from various file formats
        
        Args:
            file_path: Path to the uploaded BRD file
            
        Returns:
            Extracted text content
        """
        path = Path(file_path)
        extension = path.suffix.lower()
        
        if extension == '.pdf':
            return self._extract_from_pdf(file_path)
        elif extension in ['.docx', '.doc']:
            return self._extract_from_docx(file_path)
        elif extension == '.txt':
            return self._extract_from_txt(file_path)
        else:
            raise ValueError(f"Unsupported file format: {extension}")
    
    def _extract_from_pdf(self, file_path: str) -> str:
        """Extract text from PDF file with Groq Vision OCR fallback for image-based PDFs"""
        text = []
        
        # First, try standard text extraction
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                total_pages = len(pdf_reader.pages)
                
                for page_num, page in enumerate(pdf_reader.pages):
                    page_text = page.extract_text()
                    
                    # Check if page has meaningful text (more than just whitespace/numbers)
                    if page_text and len(page_text.strip()) > 50:
                        text.append(f"--- Page {page_num + 1} ---\n{page_text}")
                    else:
                        # Page might be image-based, mark for OCR
                        text.append(f"--- Page {page_num + 1} (OCR NEEDED) ---")
        except Exception as e:
            print(f"Standard PDF extraction failed: {e}")
        
        # Check if we got meaningful text
        combined_text = "\n\n".join(text)
        words_count = len(combined_text.split())
        
        # If we have very little text or many OCR NEEDED markers, use Groq Vision OCR
        if words_count < 100 or combined_text.count("OCR NEEDED") > 0:
            print(f"📸 PDF appears to be image-based ({words_count} words extracted)")
            print("🚀 Using FREE Groq Vision OCR (no installation required)...")
            
            try:
                from modules.groq_vision_ocr import GroqVisionOCR
                
                groq_ocr = GroqVisionOCR()
                # Enable debug mode to save images and extracted text
                ocr_text = groq_ocr.extract_text_from_pdf_pages(file_path, debug=True)
                
                if ocr_text and len(ocr_text) > len(combined_text) and not ocr_text.startswith("Error"):
                    print("✅ Groq Vision OCR successful!")
                    return ocr_text
                elif ocr_text.startswith("⚠️"):
                    # pdf2image not available, inform user
                    print(ocr_text)
                    return combined_text if combined_text.strip() else ocr_text
                    
            except Exception as e:
                print(f"⚠️ Groq Vision OCR failed: {e}")
        
        return combined_text if combined_text.strip() else "⚠️ No text extracted. This appears to be an image-based PDF. Install pdf2image for OCR support: pip install pdf2image"
    
    def _extract_with_ocr(self, file_path: str, use_mistral: bool = False) -> str:
        """Extract text from PDF using Tesseract OCR
        
        Args:
            file_path: Path to PDF file
            use_mistral: Reserved for future implementation
        """
        if not OCR_AVAILABLE:
            return "⚠️ OCR libraries not available. Install: pip install pytesseract pdf2image Pillow"
        
        try:
            # Check if poppler is available
            try:
                from pdf2image import convert_from_path
                # Test conversion with first page only
                images = convert_from_path(file_path, dpi=200, first_page=1, last_page=1)
            except Exception as poppler_error:
                if "Unable to get page count" in str(poppler_error) or "poppler" in str(poppler_error).lower():
                    return """⚠️ Poppler not found. OCR requires poppler-utils.

📥 Installation for Windows:
1. Download: https://github.com/oschwartz10612/poppler-windows/releases/
2. Extract to C:\\Program Files\\poppler
3. Add C:\\Program Files\\poppler\\Library\\bin to PATH
4. Restart the app

OR: Use a text-based PDF instead of a scanned image PDF."""
                raise
            
            print(f"📸 Using Tesseract OCR on {len(images)} page(s)...")
            
            # Now process all pages
            images = convert_from_path(file_path, dpi=200)
            
            ocr_text = []
            for page_num, image in enumerate(images):
                # Perform OCR on each page
                page_text = pytesseract.image_to_string(image, lang='eng')
                
                if page_text.strip():
                    ocr_text.append(f"--- Page {page_num + 1} (OCR) ---\n{page_text}")
                else:
                    ocr_text.append(f"--- Page {page_num + 1} (No text detected) ---")
            
            result = "\n\n".join(ocr_text)
            print(f"✅ Tesseract OCR completed: Extracted {len(result)} characters from {len(images)} pages")
            return result
            
        except Exception as e:
            error_msg = f"❌ OCR failed: {str(e)}"
            print(error_msg)
            return error_msg
    
    def _extract_from_docx(self, file_path: str) -> str:
        """Extract text from DOCX file"""
        doc = docx.Document(file_path)
        text = []
        for i, para in enumerate(doc.paragraphs):
            if para.text.strip():
                text.append(para.text)
        return "\n\n".join(text)
    
    def _extract_from_txt(self, file_path: str) -> str:
        """Extract text from TXT file"""
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    
    def parse_brd(self, file_path: str) -> dict:
        """
        Parse BRD and analyze its structure and completeness
        
        Args:
            file_path: Path to BRD file
            
        Returns:
            JSON result from Task 1 analysis
        """
        # Extract text from file
        brd_text = self.extract_text_from_file(file_path)
        
        # Load prompt template
        system_prompt = self.llm_service.load_prompt_template('task1_brd_parsing')
        
        # Prepare user prompt with BRD content
        user_prompt = f"""Analyze the following Business Requirement Document:

BRD CONTENT:
{brd_text}

Perform a thorough analysis and return the JSON structure as specified."""
        
        # Execute analysis via Groq
        result = self.llm_service.execute_prompt(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            temperature=0.2  # Lower for analytical task
        )
        
        return result
