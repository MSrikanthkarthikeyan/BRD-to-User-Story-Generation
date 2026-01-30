"""
Task 6: Output Transformation Module
Transforms user stories into export-ready structures
"""
import json
from modules.groq_service import GroqService

class OutputTransformer:
    """Transform user stories for multiple export formats"""
    
    def __init__(self):
        self.groq_service = GroqService()
    
    def transform_for_export(self, stories: dict, context: dict) -> dict:
        """
        Transform user stories into format-specific structures
        
        Args:
            stories: Result from Task 4 (user story generation)
            context: Result from Task 3 (context synthesis)
            
        Returns:
            JSON result with structures for PDF, Excel, Word, and TXT
        """
        # Load prompt template
        system_prompt = self.groq_service.load_prompt_template('task6_transformation')
        
        # Prepare transformation input
        user_prompt = f"""Transform the following user stories into export-ready structures.

BUSINESS CONTEXT:
{json.dumps(context.get('business_context', {}), indent=2)}

USER STORIES:
{json.dumps(stories, indent=2)}

Create structured formats for PDF, Excel, Word, and TXT exports. Return the JSON structure as specified."""
        
        # Execute transformation via Groq
        result = self.groq_service.execute_prompt(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            temperature=0.2
        )
        
        return result
