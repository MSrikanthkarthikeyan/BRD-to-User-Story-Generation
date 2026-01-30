"""
Google Gemini Service Wrapper
Handles all interactions with Google Gemini API
"""
import json
import time
import google.generativeai as genai
from config import Config

class GeminiService:
    """Service for interacting with Google Gemini"""
    
    def __init__(self):
        """Initialize Gemini client"""
        if not Config.is_configured():
            missing = Config.validate()
            raise ValueError(f"Missing configuration: {', '.join(missing)}")
        
        genai.configure(api_key=Config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(Config.GEMINI_MODEL)
    
    def execute_prompt(
        self, 
        system_prompt: str, 
        user_prompt: str, 
        temperature: float = None,
        max_retries: int = 3
    ) -> dict:
        """
        Execute a prompt and return validated JSON response
        
        Args:
            system_prompt: System role instructions
            user_prompt: User content/question
            temperature: Model temperature (default from config)
            max_retries: Number of retry attempts on failure
            
        Returns:
            Parsed JSON response
            
        Raises:
            Exception: If API call fails after retries or JSON is invalid
        """
        if temperature is None:
            temperature = Config.DEFAULT_TEMPERATURE
        
        # Combine system and user prompts for Gemini
        combined_prompt = f"""{system_prompt}

{user_prompt}

IMPORTANT: Return ONLY valid JSON. No markdown, no code blocks, no additional text."""
        
        for attempt in range(max_retries):
            try:
                # Configure generation
                generation_config = genai.GenerationConfig(
                    temperature=temperature,
                    max_output_tokens=Config.MAX_TOKENS,
                )
                
                response = self.model.generate_content(
                    combined_prompt,
                    generation_config=generation_config
                )
                
                # Extract and parse JSON
                content = response.text.strip()
                
                # Remove markdown code blocks if present
                if content.startswith("```json"):
                    content = content[7:]
                if content.startswith("```"):
                    content = content[3:]
                if content.endswith("```"):
                    content = content[:-3]
                content = content.strip()
                
                result = json.loads(content)
                
                # Add metadata
                result["_metadata"] = {
                    "model": Config.GEMINI_MODEL,
                    "attempt": attempt + 1
                }
                
                return result
                
            except json.JSONDecodeError as e:
                if attempt == max_retries - 1:
                    raise Exception(f"Invalid JSON response after {max_retries} attempts: {str(e)}")
                time.sleep(1)  # Wait before retry
                
            except Exception as e:
                if attempt == max_retries - 1:
                    raise Exception(f"API call failed after {max_retries} attempts: {str(e)}")
                time.sleep(2 ** attempt)  # Exponential backoff
        
        raise Exception("Unexpected error in execute_prompt")
    
    def load_prompt_template(self, task_name: str) -> str:
        """
        Load a prompt template from the prompts directory
        
        Args:
            task_name: Name of the task (e.g., 'task1_brd_parsing')
            
        Returns:
            Prompt template content
        """
        prompt_file = Config.PROMPTS_DIR / f"{task_name}.txt"
        
        if not prompt_file.exists():
            raise FileNotFoundError(f"Prompt template not found: {prompt_file}")
        
        return prompt_file.read_text(encoding='utf-8')
