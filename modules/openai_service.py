"""
Azure OpenAI Service Wrapper
Handles all interactions with Azure OpenAI API
"""
import json
import time
from openai import AzureOpenAI
from config import Config

class OpenAIService:
    """Service for interacting with Azure OpenAI"""
    
    def __init__(self):
        """Initialize Azure OpenAI client"""
        if not Config.is_configured():
            missing = Config.validate()
            raise ValueError(f"Missing configuration: {', '.join(missing)}")
        
        self.client = AzureOpenAI(
            api_key=Config.AZURE_OPENAI_API_KEY,
            api_version=Config.AZURE_OPENAI_API_VERSION,
            azure_endpoint=Config.AZURE_OPENAI_ENDPOINT
        )
        self.deployment = Config.AZURE_OPENAI_DEPLOYMENT
    
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
                response = self.client.chat.completions.create(
                    model=self.deployment,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=temperature,
                    max_tokens=Config.MAX_TOKENS,
                    response_format={"type": "json_object"}  # Enforce JSON output
                )
                
                # Extract and parse JSON
                content = response.choices[0].message.content
                result = json.loads(content)
                
                # Track token usage
                usage = response.usage
                result["_metadata"] = {
                    "prompt_tokens": usage.prompt_tokens,
                    "completion_tokens": usage.completion_tokens,
                    "total_tokens": usage.total_tokens
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
