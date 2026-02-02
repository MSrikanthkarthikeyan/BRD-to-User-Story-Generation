"""
Combined Processor Module
Combines requirement extraction, context synthesis, and story generation into a single API call
This reduces total API calls from 3 to 1, saving approximately 30-40 seconds
"""

import json
from modules.llm_service import LLMService


class CombinedProcessor:
    """
    Processes BRD in a single comprehensive pass:
    1. Requirement Extraction
    2. Context Synthesis
    3. User Story Generation
    
    This replaces 3 sequential API calls with 1 comprehensive call.
    """
    
    def __init__(self):
        self.llm_service = LLMService()
    
    def process_comprehensive(self, brd_text: str, parsing_result: dict) -> dict:
        """
        Perform comprehensive processing in a single API call
        
        Args:
            brd_text: Full text extracted from BRD
            parsing_result: Structure analysis from BRD parser
            
        Returns:
            Comprehensive JSON with requirements, context, and user_stories
        """
        # Load combined prompt template
        system_prompt = self.llm_service.load_prompt_template('combined_processing')
        
        # Prepare comprehensive user prompt
        user_prompt = f"""Perform comprehensive analysis of the following BRD.

EXTRACT requirements, SYNTHESIZE context, and GENERATE user stories ALL IN ONE PASS.

BRD STRUCTURE ANALYSIS:
{json.dumps(parsing_result, indent=2)}

FULL BRD TEXT:
{brd_text}

Return the complete JSON structure with ALL sections:
- requirements (business_objectives, stakeholders, functional_requirements, non_functional_requirements, constraints, assumptions, risks, dependencies)
- context (business_context, user_personas, system_boundaries, external_integrations, success_metrics)
- user_stories (complete stories with acceptance criteria, risks, steps)
- epic_groupings
- traceability_matrix

Be thorough and comprehensive. This is a single-pass analysis."""
        
        print("🚀 Starting comprehensive single-pass processing...")
        print(f"📊 BRD length: {len(brd_text)} characters")
        
        # Execute comprehensive prompt with higher temperature for creativity in story generation
        result = self.llm_service.execute_prompt(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            temperature=0.4,  # Balance between consistency and creativity
            max_tokens=16000  # Larger response needed for comprehensive output
        )
        
        print(f"✅ Comprehensive processing complete")
        print(f"📝 Generated {len(result.get('user_stories', []))} user stories")
        print(f"📦 Extracted {len(result.get('requirements', {}).get('functional_requirements', []))} functional requirements")
        
        # Validate structure
        if not self._validate_comprehensive_output(result):
            raise ValueError("Comprehensive output validation failed - missing required sections")
        
        return result
    
    def _validate_comprehensive_output(self, result: dict) -> bool:
        """
        Validate that comprehensive output has all required sections
        
        Args:
            result: Output from comprehensive processing
            
        Returns:
            True if valid, False otherwise
        """
        # Check top-level keys
        required_keys = ['requirements', 'context', 'user_stories']
        for key in required_keys:
            if key not in result:
                print(f"❌ Missing required key: {key}")
                return False
        
        # Check requirements sub-keys
        req_keys = ['functional_requirements', 'business_objectives', 'stakeholders']
        for key in req_keys:
            if key not in result['requirements']:
                print(f"⚠️ Missing requirements.{key} (non-critical)")
        
        # Check context sub-keys
        ctx_keys = ['business_context', 'user_personas', 'system_boundaries']
        for key in ctx_keys:
            if key not in result['context']:
                print(f"⚠️ Missing context.{key} (non-critical)")
        
        # Check user_stories is a list
        if not isinstance(result['user_stories'], list):
            print("❌ user_stories must be a list")
            return  False
        
        # Check we have at least one story
        if len(result['user_stories']) == 0:
            print("⚠️ No user stories generated")
            return False
        
        print(f"✅ Validation passed: {len(result['user_stories'])} stories, "
              f"{len(result['requirements'].get('functional_requirements', []))} FRs")
        
        return True
    
    def split_comprehensive_result(self, comprehensive_result: dict) -> tuple:
        """
        Split comprehensive result into separate components for compatibility
        
        Args:
            comprehensive_result: Combined output from process_comprehensive()
            
        Returns:
            Tuple of (requirements, context, stories)
        """
        requirements = comprehensive_result.get('requirements', {})
        context = comprehensive_result.get('context', {})
        stories = {
            'user_stories': comprehensive_result.get('user_stories', []),
            'epic_groupings': comprehensive_result.get('epic_groupings', []),
            'traceability_matrix': comprehensive_result.get('traceability_matrix', [])
        }
        
        return requirements, context, stories
