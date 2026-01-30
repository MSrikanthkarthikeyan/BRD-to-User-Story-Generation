"""
Groq API Service Wrapper
Handles all interactions with Groq API
"""
import json
import time
from groq import Groq
from config import Config

class GroqService:
    """Service for interacting with Groq API"""
    
    def __init__(self):
        """Initialize Groq client"""
        if not Config.is_configured():
            missing = Config.validate()
            raise ValueError(f"Missing configuration: {', '.join(missing)}")
        
        self.client = Groq(api_key=Config.GROQ_API_KEY)
    
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
        
        for attempt in range(max_retries):
            try:
                # Create chat completion
                chat_completion = self.client.chat.completions.create(
                    messages=[
                        {
                            "role": "system",
                            "content": system_prompt + "\n\nCRITICAL: You MUST return ONLY valid, complete JSON. Ensure all strings are properly closed with quotes. No markdown formatting."
                        },
                        {
                            "role": "user",
                            "content": user_prompt
                        }
                    ],
                    model=Config.GROQ_MODEL,
                    temperature=temperature,
                    max_tokens=8000,  # Increased to handle large responses
                )
                
                # Extract content
                content = chat_completion.choices[0].message.content.strip()
                
                # Remove markdown code blocks if present
                if content.startswith("```json"):
                    content = content[7:]
                if content.startswith("```"):
                    content = content[3:]
                if content.endswith("```"):
                    content = content[:-3]
                content = content.strip()
                
                # Try to repair common JSON issues
                # Fix unterminated strings by finding the last valid closing brace
                if not content.endswith('}'):
                    # Try to find the last complete object
                    last_brace = content.rfind('}')
                    if last_brace > 0:
                        content = content[:last_brace + 1]
                
                # Parse JSON
                try:
                    result = json.loads(content)
                except json.JSONDecodeError as e:
                    # Try to extract valid JSON from the response
                    # Find the first { and last }
                    first_brace = content.find('{')
                    last_brace = content.rfind('}')
                    
                    if first_brace >= 0 and last_brace > first_brace:
                        extracted = content[first_brace:last_brace + 1]
                        try:
                            result = json.loads(extracted)
                        except:
                            raise e
                    else:
                        raise e
                
                # Add metadata
                result["_metadata"] = {
                    "model": Config.GROQ_MODEL,
                    "attempt": attempt + 1,
                    "tokens": {
                        "prompt": chat_completion.usage.prompt_tokens,
                        "completion": chat_completion.usage.completion_tokens,
                        "total": chat_completion.usage.total_tokens
                    }
                }
                
                return result
                
            except json.JSONDecodeError as e:
                if attempt == max_retries - 1:
                    # On final attempt, save the problematic response for debugging
                    print(f"DEBUG: Failed JSON content:\n{content[:500]}...")
                    raise Exception(f"Invalid JSON response after {max_retries} attempts: {str(e)}")
                print(f"Attempt {attempt + 1} failed with JSON error, retrying...")
                time.sleep(2)  # Wait before retry
                
            except Exception as e:
                if attempt == max_retries - 1:
                    raise Exception(f"API call failed after {max_retries} attempts: {str(e)}")
                print(f"Attempt {attempt + 1} failed, retrying...")
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
