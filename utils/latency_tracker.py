import time
from functools import wraps
from utils.logger import get_logger

logger = get_logger(__name__)

def track_latency(module_name: str):
    """
    Decorator to measure and log the execution time of a function.

    Args:
        module_name (str): Name of the module or context being timed (e.g., __name__).

    Returns:
        The original function's return value.
    """
    
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.perf_counter()
            result = func(*args, **kwargs)
            end_time = time.perf_counter()
            duration = end_time - start_time
            logger.info("Duration for %s: %.6f second(s)", module_name, duration)
            return result
        return wrapper
    return decorator
