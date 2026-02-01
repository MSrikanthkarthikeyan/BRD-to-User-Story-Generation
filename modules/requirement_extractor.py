"""
Task 2: Requirement Extraction Module
Extracts and categorizes requirements from parsed BRD
"""
from modules.llm_service import LLMService

class RequirementExtractor:
    """Extract and categorize requirements from BRD"""
    
    def __init__(self):
        self.llm_service = LLMService()
    
    def extract_requirements(self, brd_text: str, parsing_result: dict) -> dict:
        """
        Extract requirements from BRD with full traceability
        
        Args:
            brd_text: Raw BRD text content
            parsing_result: Result from Task 1 (BRD parsing)
            
        Returns:
            JSON result with categorized requirements
        """
        # Load prompt template
        system_prompt = self.llm_service.load_prompt_template('task2_extraction')
        
        # Prepare user prompt with BRD content and parsing context
        user_prompt = f"""Extract requirements from the following BRD.

BRD ANALYSIS CONTEXT:
Completeness Score: {parsing_result.get('completeness_score', 'N/A')}
Detected Sections: {', '.join([s['section_name'] for s in parsing_result.get('detected_sections', [])])}

BRD CONTENT:
{brd_text}

Extract all requirements with precision, traceability, and confidence levels. Return the JSON structure as specified."""
        
        # Execute extraction via Groq
        result = self.llm_service.execute_prompt(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            temperature=0.2
        )
        
        return result
