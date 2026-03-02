import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    # Project Paths
    ROOT_DIR = Path(__file__).parent.parent.parent
    DATA_DIR = ROOT_DIR / "data"
    CONFIG_DIR = ROOT_DIR / "config"
    OUTPUT_DIR = DATA_DIR / "outputs"
    
    # API Keys
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    
    # Provider Settings
    DEFAULT_LLM_PROVIDER = os.getenv("DEFAULT_LLM_PROVIDER", "openai")
    LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4o")
    PROMPT_VERSION = os.getenv("PROMPT_VERSION", "v1")
    
    # OCR Settings
    OCR_ENGINE = os.getenv("OCR_ENGINE", "vision_llm")
    
    # Validation Thresholds
    CONFIDENCE_THRESHOLD = float(os.getenv("CONFIDENCE_THRESHOLD", 0.85))
    
    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    ENABLE_RAW_LOGGING = os.getenv("ENABLE_RAW_LOGGING", "true").lower() == "true"

    @classmethod
    def validate(cls):
        """Ensure critical environment variables are set."""
        if cls.DEFAULT_LLM_PROVIDER == "openai" and not cls.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is required for OpenAI provider.")
        if cls.DEFAULT_LLM_PROVIDER == "anthropic" and not cls.ANTHROPIC_API_KEY:
            raise ValueError("ANTHROPIC_API_KEY is required for Anthropic provider.")

config = Config()
