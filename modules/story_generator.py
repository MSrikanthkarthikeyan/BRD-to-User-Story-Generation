"""
Task 4: User Story Generation Module
Converts requirements into enterprise Agile user stories
"""
import json
from modules.llm_service import LLMService

class StoryGenerator:
    """Generate enterprise-standard user stories"""
    
    def __init__(self):
        self.llm_service = LLMService()
    
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
        system_prompt = self.llm_service.load_prompt_template('task4_generation')
        
        # Prepare user prompt
        # Map original parameters to new variable names used in the prompt construction
        context_data = context
        requirements_list = requirements.get('functional_requirements', []) + requirements.get('non_functional_requirements', [])

        # DEBUG: Print requirements before formatting
        print("=" * 80)
        print("DEBUG: STORY_GENERATOR - FORMATTING REQUIREMENTS")
        print(f"Total requirements to format: {len(requirements_list)}")
        if requirements_list:
            print("First requirement structure:")
            print(f"  Keys: {requirements_list[0].keys()}")
            print(f"  Sample: {requirements_list[0]}")
        print("=" * 80)

        # Format requirements for clear presentation
        # FIX: Use correct field names - 'description' and 'category', not 'requirement' and 'type'!
        requirements_text = "\n".join([
            f"- [{req.get('requirement_id', 'REQ')}] {req.get('category', 'General')}: {req.get('description', 'N/A')}"
            for req in requirements_list
        ])
        
        # DEBUG: Print formatted requirements
        print("=" * 80)
        print("DEBUG: FORMATTED REQUIREMENTS TEXT")
        print(f"Length: {len(requirements_text)} characters")
        print("First 500 characters:")
        print(requirements_text[:500])
        print("=" * 80)
        
        # Extract project context
        project_name = context_data.get('project_overview', {}).get('project_name', 'Enterprise System')
        business_goals = context_data.get('business_objectives', {}).get('primary_goals', [])
        goals_text = "\n".join([f"- {goal}" for goal in (business_goals if isinstance(business_goals, list) else [business_goals])])
        
        # Create comprehensive user prompt
        user_prompt = f"""
INDUSTRY CONTEXT:
You are working on a project in the Energy and Utilities sector for {project_name}.

PROJECT EPIC:
Epic Name: {project_name} Implementation
Epic Goals:
{goals_text if goals_text else '- Deliver high-value business capabilities\n- Improve operational efficiency\n- Enhance user experience'}

PROJECT FEATURE:
Feature: Core System Requirements Implementation
Feature Goals:
- Implement validated functional requirements
- Ensure system reliability and performance
- Meet business stakeholder expectations

BUSINESS CONTEXT:
{context_data.get('business_overview', 'Enterprise energy management system implementation.')}

VALIDATED REQUIREMENTS TO CONVERT INTO USER STORIES:
{requirements_text}

SYNTHESIZED BUSINESS CONTEXT:
Project Overview: {context_data.get('project_overview', {}).get('description', 'System enhancement project')}

Business Objectives: {context_data.get('business_objectives', {}).get('summary', 'Improve business operations')}

Stakeholders: {', '.join(context_data.get('stakeholders', {}).get('primary', []))}

SUCCESS CRITERIA: {', '.join(context_data.get('success_criteria', {}).get('key_metrics', []))}

INSTRUCTIONS:
Generate comprehensive user stories following the SMART framework and industry best practices. Each story should:
1. Include title, user story (max 25 words), importance, context, recommended steps, 5 risks with mitigation, and acceptance criteria
2. Explain how it contributes to achieving the Epic and Feature goals stated above
3. Use natural, professional language avoiding buzzwords
4. Provide actionable implementation steps
5. Identify realistic risks and mitigation strategies
6. Create testable acceptance criteria

Return ONLY valid JSON following the specified format. No additional text or markdown.
"""
        
        # Execute generation via Groq
        result = self.llm_service.execute_prompt(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            temperature=0.4  # Slightly higher for creative story writing
        )
        
        return result
