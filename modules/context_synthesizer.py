"""
Task 3: Context Synthesis Module
Derives business context and user personas from requirements
"""
import json
from modules.llm_service import LLMService

class ContextSynthesizer:
    """Synthesize business context from extracted requirements"""
    
    def __init__(self):
        self.llm_service = LLMService()
    
    def synthesize_context(self, requirements: dict) -> dict:
        """
        Derive business context from extracted requirements
        
        Args:
            requirements: Result from Task 2 (requirement extraction)
            
        Returns:
            JSON result with business context, personas, and boundaries
        """
        # Load prompt template
        system_prompt = self.llm_service.load_prompt_template('task3_synthesis')
        
        # Prepare user prompt with requirements
        user_prompt = f"""Synthesize business context from the following extracted requirements.

EXTRACTED REQUIREMENTS:
{json.dumps(requirements, indent=2)}

Derive context, personas, boundaries, and success metrics. DO NOT add new requirements. Return the JSON structure as specified."""
        
        # Execute synthesis via Groq
        result = self.llm_service.execute_prompt(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            temperature=0.3
        )
        
        return result
