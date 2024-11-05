from typing import Dict, Any
from data.rate_cards import RATE_CARDS

def calculate_costs(metrics: Dict[str, Any]) -> Dict[str, float]:
    """
    Calculates various costs based on website complexity metrics.
    
    Args:
        metrics (Dict[str, Any]): Website complexity metrics
        
    Returns:
        Dict[str, float]: Dictionary containing cost breakdowns
    """
    complexity_multiplier = metrics['complexity_score'] / 5  # Normalize to 0-2 range
    
    # Calculate development costs
    frontend_cost = RATE_CARDS['frontend_hourly_rate'] * estimate_frontend_hours(metrics)
    backend_cost = RATE_CARDS['backend_hourly_rate'] * estimate_backend_hours(metrics)
    
    # Calculate hosting costs based on complexity
    base_hosting = RATE_CARDS['base_hosting_cost']
    hosting_cost = base_hosting * complexity_multiplier
    
    # Calculate maintenance costs
    maintenance_cost = (frontend_cost + backend_cost) * RATE_CARDS['maintenance_percentage']
    
    return {
        'development': frontend_cost + backend_cost,
        'frontend': frontend_cost,
        'backend': backend_cost,
        'hosting': hosting_cost,
        'maintenance': maintenance_cost
    }

def estimate_frontend_hours(metrics: Dict[str, Any]) -> float:
    """
    Estimates frontend development hours based on complexity metrics.
    
    Args:
        metrics (Dict[str, Any]): Website complexity metrics
        
    Returns:
        float: Estimated hours
    """
    base_hours = 40  # Base hours for a simple website
    
    additional_hours = (
        metrics['estimated_pages'] * 4 +  # 4 hours per page
        (20 if metrics['has_forms'] else 0) +  # Forms add complexity
        (30 if metrics['has_dynamic_content'] else 0)  # Dynamic content adds complexity
    )
    
    return base_hours + additional_hours

def estimate_backend_hours(metrics: Dict[str, Any]) -> float:
    """
    Estimates backend development hours based on complexity metrics.
    
    Args:
        metrics (Dict[str, Any]): Website complexity metrics
        
    Returns:
        float: Estimated hours
    """
    base_hours = 20  # Base hours for a simple backend
    
    additional_hours = (
        (40 if metrics['has_authentication'] else 0) +  # Authentication adds complexity
        (metrics['estimated_pages'] * 2) +  # API endpoints per page
        (30 if metrics['has_dynamic_content'] else 0)  # Dynamic content needs backend support
    )
    
    return base_hours + additional_hours
