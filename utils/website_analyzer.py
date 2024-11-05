import trafilatura
from typing import Dict, Any

def analyze_website(url: str) -> Dict[str, Any]:
    """
    Analyzes a website and returns complexity metrics.
    
    Args:
        url (str): Website URL to analyze
        
    Returns:
        Dict[str, Any]: Dictionary containing complexity metrics
    """
    # Download and extract content
    downloaded = trafilatura.fetch_url(url)
    content = trafilatura.extract(downloaded, include_links=True, include_images=True)
    
    if not content:
        raise Exception("Could not extract content from website")

    # Calculate complexity metrics
    metrics = {
        "content_length": len(content),
        "complexity_score": calculate_complexity_score(content),
        "estimated_pages": estimate_page_count(content),
        "has_forms": "form" in content.lower(),
        "has_authentication": any(auth_term in content.lower() 
                                for auth_term in ["login", "signin", "register"]),
        "has_dynamic_content": any(dynamic_term in content.lower() 
                                 for dynamic_term in ["javascript", "api", "ajax"]),
    }
    
    return metrics

def calculate_complexity_score(content: str) -> float:
    """
    Calculates a complexity score based on content analysis.
    
    Args:
        content (str): Website content
        
    Returns:
        float: Complexity score between 1-10
    """
    score = 1.0
    
    # Content length factors
    if len(content) > 10000:
        score += 2
    elif len(content) > 5000:
        score += 1

    # Feature detection
    if "database" in content.lower():
        score += 1
    if "api" in content.lower():
        score += 1
    if "authentication" in content.lower():
        score += 1
    if "payment" in content.lower():
        score += 2
    
    return min(score, 10.0)

def estimate_page_count(content: str) -> int:
    """
    Estimates the number of pages based on content analysis.
    
    Args:
        content (str): Website content
        
    Returns:
        int: Estimated number of pages
    """
    # Simple estimation based on content length and menu items
    base_pages = 5  # Assuming minimum pages (home, about, contact, etc.)
    content_pages = len(content) // 3000  # Rough estimate of one page per 3000 chars
    
    return base_pages + content_pages
