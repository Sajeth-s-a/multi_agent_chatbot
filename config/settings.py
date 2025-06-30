from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    Application settings for the chatbot framework.
    Loads environment variables from .env file.
    """
    ANTHROPIC_API_KEY: str

    model_config = SettingsConfigDict(env_file='.env', extra='ignore')

settings = Settings()