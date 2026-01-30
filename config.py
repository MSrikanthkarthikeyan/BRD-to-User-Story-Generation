"""
Configuration management for BRD to User Story Generator
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Application configuration"""
    
    # Groq API Configuration
    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
    GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")  # Fast and accurate
    
    # Application Settings
    APP_NAME = "BRD to User Story Generator"
    APP_BRAND = "Embridge"
    
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
        if not cls.GROQ_API_KEY:
            missing.append("GROQ_API_KEY")
        
        return missing
    
    @classmethod
    def is_configured(cls):
        """Check if all required config is present"""
        return len(cls.validate()) == 0
