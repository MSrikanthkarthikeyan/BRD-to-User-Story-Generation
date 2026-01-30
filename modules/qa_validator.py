"""
Task 5: QA Validation Module
Validates user stories for quality and coverage
"""
import json
from modules.groq_service import GroqService

class QAValidator:
    """Validate user stories for quality, coverage, and testability"""
    
    def __init__(self):
        self.groq_service = GroqService()
    
    def validate_stories(self, requirements: dict, stories: dict) -> dict:
        """
        Validate user stories without modifying them
        
        Args:
            requirements: Result from Task 2 (requirement extraction)
            stories: Result from Task 4 (user story generation)
            
        Returns:
            JSON result with validation findings and quality score
        """
        # Load prompt template
        system_prompt = self.groq_service.load_prompt_template('task5_validation')
        
        # Prepare validation context
        user_prompt = f"""Validate the following user stories against the original requirements.

ORIGINAL REQUIREMENTS:
Total Functional Requirements: {len(requirements.get('functional_requirements', []))}
Total Non-Functional Requirements: {len(requirements.get('non_functional_requirements', []))}

REQUIREMENTS DATA:
{json.dumps(requirements, indent=2)}

GENERATED USER STORIES:
Total Stories: {len(stories.get('user_stories', []))}

STORIES DATA:
{json.dumps(stories, indent=2)}

Validate for coverage, redundancy, ambiguity, and testability. Flag issues only. Return the JSON structure as specified."""
        
        # Execute validation via Groq
        result = self.groq_service.execute_prompt(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            temperature=0.2  # Lower for analytical validation
        )
        
        return result
