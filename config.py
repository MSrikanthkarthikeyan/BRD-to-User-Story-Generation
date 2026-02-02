"""
Configuration management for BRD to User Story Generator
Loads API keys and settings from .env file
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file in project root
env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)

class Config:
    """Application configuration"""
    
    # Azure OpenAI Configuration (Primary LLM)
    AZURE_OPENAI_KEY = os.getenv("AZURE_OPENAI_KEY", "")
    AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT", "")
    AZURE_OPENAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4o")
    AZURE_OPENAI_MODEL = os.getenv("AZURE_OPENAI_MODEL", "gpt-4o")
    AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION", "2024-08-01-preview")
    
    # Application Settings
    APP_NAME = "BRD to User Story Generator"
    APP_BRAND = "Enbridge"
    
    # UI Theme (Embridge branding)
    THEME_PRIMARY_COLOR = "#FFD700"  # Yellow
    THEME_BACKGROUND_COLOR = "#FFFFFF"  # White
    THEME_SECONDARY_BACKGROUND = "#FFFEF0"  # Light yellow tint
    THEME_TEXT_COLOR = "#1F1F1F"  # Dark gray
    
    # Directories
    BASE_DIR = Path(__file__).parent
    EXPORTS_DIR = BASE_DIR / "exports"
    ASSETS_DIR = BASE_DIR / "assets"
    PROMPTS_DIR = BASE_DIR / "prompts"
    
    # Ensure directories exist
    EXPORTS_DIR.mkdir(exist_ok=True)
    ASSETS_DIR.mkdir(exist_ok=True)
    PROMPTS_DIR.mkdir(exist_ok=True)
    
    # OpenAI Model Parameters
    DEFAULT_TEMPERATURE = 0.3  # Lower for more focused outputs
    MAX_TOKENS = 4000
    
    @classmethod
    def validate(cls):
        """Validate required configuration"""
        missing = []
        if not cls.AZURE_OPENAI_KEY:
            missing.append("AZURE_OPENAI_KEY")
        if not cls.AZURE_OPENAI_ENDPOINT:
            missing.append("AZURE_OPENAI_ENDPOINT")
        # Removed GROQ_API_KEY requirement - now using Azure only
        
        return missing
    
    @classmethod
    def is_configured(cls):
        """Check if all required config is present"""
        return len(cls.validate()) == 0
