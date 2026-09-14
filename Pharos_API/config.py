from pydantic_settings import BaseSettings
from pydantic import field_validator
from typing import List, Optional
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    """
    Application settings loaded from environment variables
    """
    
    # Pharos API Configuration
    pharos_api_url: str = ""
    pharos_api_timeout: int = 30
    pharos_retry_attempts: int = 3
    
    # FastAPI Application Settings
    app_title: str = "Pharos API Gateway"
    app_description: str = "FastAPI service to connect Galaxy with Pharos GraphQL API"
    app_version: str = "1.0.0"
    
    # Server Configuration
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = False
    
    # Pagination Defaults
    default_page_size: int = 10
    max_page_size: int = 100
    
    # Rate Limiting (requests per minute)
    rate_limit_per_minute: int = 60
    
    # Cache Settings (for future implementation)
    cache_enabled: bool = True
    cache_ttl_seconds: int = 300  # 5 minutes
    
    # Galaxy Integration Settings
    supported_output_formats: List[str] = ["json", "csv", "tsv"]
    default_output_format: str = "json"
    
    # Query Configuration
    max_search_results: int = 1000
    default_target_fields: str = "basic"  # basic, detailed, full
    
    # Logging Configuration
    log_level: str = "INFO"
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    @field_validator('pharos_api_url')
    @classmethod
    def validate_pharos_url(cls, v):
        if not v:
            raise ValueError('PHAROS_API_URL environment variable is required')
        if not v.startswith(('http://', 'https://')):
            raise ValueError('PHAROS_API_URL must be a valid HTTP/HTTPS URL')
        return v.rstrip('/')
    
    @field_validator('pharos_api_timeout')
    @classmethod
    def validate_timeout(cls, v):
        if v <= 0:
            raise ValueError('API timeout must be positive')
        return v
    
    @field_validator('max_page_size')
    @classmethod
    def validate_page_size(cls, v):
        if v > 1000:
            raise ValueError('Maximum page size cannot exceed 1000')
        return v
    
    @field_validator('supported_output_formats')
    @classmethod
    def validate_output_formats(cls, v):
        allowed_formats = ["json", "csv", "tsv", "xml"]
        for format_type in v:
            if format_type not in allowed_formats:
                raise ValueError(f'Unsupported output format: {format_type}')
        return v
    
    class Config:
        env_file = ".env"
        case_sensitive = False

# Create global settings instance
settings = Settings()

# Development vs Production configuration
def get_settings() -> Settings:
    """
    Factory function to get settings instance
    Useful for dependency injection and testing
    """
    return settings

# Configuration validation
def validate_configuration():
    """
    Validate that all required configuration is present and correct
    Call this at application startup
    """
    try:
        # Test that we can create settings instance
        config = Settings()
        
        print(f"✅ Configuration loaded successfully")
        print(f"   Pharos API URL: {config.pharos_api_url}")
        print(f"   Server: {config.host}:{config.port}")
        print(f"   Debug mode: {config.debug}")
        print(f"   Rate limit: {config.rate_limit_per_minute} req/min")
        
        return True
        
    except Exception as e:
        print(f"❌ Configuration error: {str(e)}")
        return False

# Helper functions for common configuration tasks
def get_pharos_headers() -> dict:
    """Get standard headers for Pharos API requests"""
    return {
        "Content-Type": "application/json",
        "User-Agent": f"{settings.app_title}/{settings.app_version}"
    }

def get_pagination_params(page: int = 1, size: int = None) -> dict:
    """Get standardized pagination parameters"""
    size = size or settings.default_page_size
    size = min(size, settings.max_page_size)
    skip = (page - 1) * size
    
    return {
        "skip": skip,
        "limit": size
    }

if __name__ == "__main__":
    # Test configuration when run directly
    print("Testing configuration...")
    validate_configuration()