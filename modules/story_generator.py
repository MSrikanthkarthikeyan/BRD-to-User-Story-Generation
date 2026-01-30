"""
Task 4: User Story Generation Module
Converts requirements into enterprise Agile user stories
"""
import json
from modules.groq_service import GroqService

class StoryGenerator:
    """Generate enterprise-standard user stories"""
    
    def __init__(self):
        self.groq_service = GroqService()
    
    def generate_stories(self, requirements: dict, context: dict) -> dict:
        """
        Generate user stories from requirements and context
        
        Args:
            requirements: Result from Task 2 (requirement extraction)
            context: Result from Task 3 (context synthesis)
            
        Returns:
            JSON result with user stories and epic groupings
        """
        # Load prompt template
        system_prompt = self.groq_service.load_prompt_template('task4_generation')
        
        # Prepare user prompt
        user_prompt = f"""Generate enterprise-standard Agile user stories from the following inputs.

BUSINESS CONTEXT:
{json.dumps(context.get('business_context', {}), indent=2)}

USER PERSONAS:
{json.dumps(context.get('user_personas', []), indent=2)}

REQUIREMENTS:
Functional Requirements: {len(requirements.get('functional_requirements', []))} items
Non-Functional Requirements: {len(requirements.get('non_functional_requirements', []))} items

FULL REQUIREMENTS DATA:
{json.dumps(requirements, indent=2)}

Generate comprehensive user stories with full traceability. Return the JSON structure as specified."""
        
        # Execute generation via Groq
        result = self.groq_service.execute_prompt(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            temperature=0.4  # Slightly higher for creative story writing
        )
        
        return result
