"""Default configuration settings."""
from functools import lru_cache



class Settings():
    """Default BaseSettings."""

    env_name: str = "development"
    base_url: str = "http://localhost:8000/"
    # base_url: str = "https://ez-ly.onrender.com/"
    db_url: str = "sqlite:///./Ezzy_Url_Shortener.sqlite"

    # Postgreqsl specific
    # db_name: str = "txuvnlmz" #Database name
    # db_address: str = "ruby.db.elephantsql.com"
    # db_port: str = "5432"
    # db_user: str = "txuvnlmz"
    # db_pw: str = "DjcJqOSw9ZWZy7HM38PD3DmWWrv8HFoK" # Database password

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
        settings.db_url = "postgresql://txuvnlmz:DjcJqOSw9ZWZy7HM38PD3DmWWrv8HFoK@ruby.db.elephantsql.com/txuvnlmz"
        settings.base_url = "https://ez-ly.onrender.com"

    return settings
