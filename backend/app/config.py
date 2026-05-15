"""Configuration module"""

from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    """Application settings"""
    
    # Telegram Bot
    bot_token: str
    webapp_url: str
    admin_id: int
    
    # Database
    database_url: str = "sqlite:///./nft_trading.db"
    
    # Server
    debug: bool = False
    host: str = "0.0.0.0"
    port: int = 8000
    
    # API
    api_prefix: str = "/api"
    api_version: str = "v1"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Load settings
settings = Settings()
