"""Helper functions to generate Keys."""
import secrets
import string
from sqlalchemy.orm import Session
from utils import crud

#function 1
def create_random_key(length: int = 5) -> str:
    """Return a random key of the specified length."""
    chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
    return "".join(secrets.choice(chars) for _ in range(length))

#function 2
def create_unique_random_key(db:Session) -> str:
    """Create a guaranteed random key."""
    url_key = create_random_key()
    while crud.get_url_by_key(url_key, db):
        url_key = create_random_key()
    return url_key

