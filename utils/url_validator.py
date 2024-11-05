import re
from urllib.parse import urlparse

def validate_url(url: str) -> bool:
    """
    Validates if the given string is a proper URL.
    
    Args:
        url (str): URL to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc]) and result.scheme in ['http', 'https']
    except:
        return False
