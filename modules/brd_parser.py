"""
Task 1: BRD Parsing Module
Analyzes uploaded BRD documents for structure and completeness
"""
import PyPDF2
import docx
from pathlib import Path
from modules.groq_service import GroqService

class BRDParser:
    """Parse and analyze Business Requirement Documents"""
    
    def __init__(self):
        self.groq_service = GroqService()
    
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
        """Extract text from PDF file"""
        text = []
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page_num, page in enumerate(pdf_reader.pages):
                page_text = page.extract_text()
                text.append(f"--- Page {page_num + 1} ---\n{page_text}")
        return "\n\n".join(text)
    
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
        system_prompt = self.groq_service.load_prompt_template('task1_brd_parsing')
        
        # Prepare user prompt with BRD content
        user_prompt = f"""Analyze the following Business Requirement Document:

BRD CONTENT:
{brd_text}

Perform a thorough analysis and return the JSON structure as specified."""
        
        # Execute analysis via Groq
        result = self.groq_service.execute_prompt(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            temperature=0.2  # Lower for analytical task
        )
        
        return result
