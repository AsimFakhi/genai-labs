"""
Application-wide configuration.

This module is intentionally small. It only contains settings that are
shared across the entire repository.
"""

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    openai_api_key: str = Field(description="OpenAI API key")
    openrouter_api_key: str = Field(description="OpenRouter API key")
    nvidia_api_key: str = Field(description="NvidNVIDIAia API key")
    
    openrouter_url:str
    nvidia_url:str
    nvidia_chat_url:str

    gpt_nano: str
    
    or_router:str
    or_gpt_oss_120:str
    
    nv_nemotron_ultra:str
    nv_gpt_20:str
    nv_gpt_120:str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    """Return a cached Settings instance."""
    return Settings()