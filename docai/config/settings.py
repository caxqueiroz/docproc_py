from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "sqlite:///./docai.db"
    
    # Storage
    STORAGE_PATH: str = "storage"
    
    @property
    def final_storage_path(self) -> Path:
        return Path(self.STORAGE_PATH)
    
    # OpenAI
    OPENAI_API_KEY: str = ""
    
    # File Processing
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # Default: 10MB
    SUPPORTED_FORMATS: list = ["pdf", "png", "jpg", "jpeg", "docx", "xlsx"]
    
    # API
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
