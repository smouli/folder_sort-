import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings:
    """Application settings and configuration"""
    
    # API Keys
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
    LLAMAPARSE_API_KEY: str = os.getenv("LLAMAPARSE_API_KEY")
    
    USER_ID: str = os.getenv("USER_ID", "default_user")
    
    def __init__(self):
        # Set OpenAI API key in environment for langchain
        if self.OPENAI_API_KEY:
            os.environ["OPENAI_API_KEY"] = self.OPENAI_API_KEY
        else:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        
        if not self.LLAMAPARSE_API_KEY:
            raise ValueError("LLAMAPARSE_API_KEY environment variable is required")

# Create settings instance
settings = Settings()
