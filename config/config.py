"""Default configuration settings."""
from functools import lru_cache

class Settings():
    """Default BaseSettings."""

    env_name: str = "development"
    base_url: str = "http://localhost:8000/"
    db_url: str = "sqlite:///./Ezzy_Url_Shortener.sqlite"

    # default to SQLite
    db_backend: str = "postgresql" #change to 'postgresql' for postgres database
    
    #openai tags
    tags = [
        {'name': 'auth',
        'description': 'Routes related to Authentication and Authorization'
        },
        {'name': 'user',
        'description': 'Routes related to User Account creation'
        },
        {'name': 'url',
        'description': 'Routes related to URL adding and listing'
        },
        {'name': 'pages',
        'description': 'Routes related to browsing web pages'
        }
    ]
    
    SECRET_KEY = "ezzyscissorbdbc97f82bfe593d1e45cec19ad2591af315096665512564df9af"
    ALGORITHM = "HS256"
    
    class Config:
        """Load env variables from .env file."""
        env_file = ".env"


@lru_cache
def get_settings() -> Settings:
    """Return the current settings."""
    settings = Settings()
    if settings.db_backend == "postgresql":
        settings.db_url = "postgresql://ofqcobrn:zGAxW-IDKlJg4F2sYwCv-NfYZpYDV3ag@ruby.db.elephantsql.com/ofqcobrn"
        settings.base_url = "https://ez-ly.onrender.com/"

    return settings
