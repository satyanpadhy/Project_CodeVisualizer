from functools import wraps
from tenacity import retry, stop_after_attempt, wait_exponential
import logging
from typing import Type, Tuple, Optional, Callable

class AnalyzerError(Exception):
    """Base exception class for analyzer errors."""
    pass

class ParseError(AnalyzerError):
    """Raised when parsing a file fails."""
    pass

class CacheError(AnalyzerError):
    """Raised when cache operations fail."""
    pass

class VisualizationError(AnalyzerError):
    """Raised when visualization generation fails."""
    pass

def with_error_handling(error_types: Tuple[Type[Exception], ...],
                       max_retries: int = 3,
                       logger: Optional[logging.Logger] = None):
    """Decorator for handling errors with retry logic."""
    def decorator(func: Callable):
        @retry(
            stop=stop_after_attempt(max_retries),
            wait=wait_exponential(multiplier=1, min=4, max=10),
            retry=lambda e: isinstance(e, error_types)
        )
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except error_types as e:
                if logger:
                    logger.error(f"Error in {func.__name__}: {str(e)}")
                raise
            except Exception as e:
                if logger:
                    logger.critical(f"Unexpected error in {func.__name__}: {str(e)}")
                raise AnalyzerError(f"Unexpected error: {str(e)}")
        return wrapper
    return decorator

def setup_error_handlers(logger: logging.Logger):
    """Configure global error handlers."""
    def handle_uncaught_exception(exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            # Call the default handler for keyboard interrupt
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return
        
        logger.critical("Uncaught exception:", exc_info=(exc_type, exc_value, exc_traceback))
    
    import sys
    sys.excepthook = handle_uncaught_exception