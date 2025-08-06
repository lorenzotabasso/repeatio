from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Audio Microservice"
    
    # File Storage
    UPLOAD_DIR: str = "uploads"
    OUTPUT_DIR: str = "outputs"
    
    # Audio Settings
    DEFAULT_PAUSE_DURATION: int = 5000  # milliseconds
    DEFAULT_SILENCE_DURATION: int = 1000  # milliseconds
    
    # Supported Languages
    SUPPORTED_LANGUAGES = {
        'it': 'Italian',
        'ru': 'Russian',
        'en': 'English',
        'es': 'Spanish',
        'fr': 'French',
        'de': 'German',
        'pt': 'Portuguese',
        'ja': 'Japanese',
        'ko': 'Korean',
        'zh': 'Chinese'
    }
    
    class Config:
        env_file = ".env"

settings = Settings()

# Create directories if they don't exist
Path(settings.UPLOAD_DIR).mkdir(exist_ok=True)
Path(settings.OUTPUT_DIR).mkdir(exist_ok=True) 