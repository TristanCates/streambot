from functools import wraps
from typing import Callable

def handle_command_errors(func: Callable) -> Callable:
    """Decorator to handle common command error patterns."""
    @wraps(func)
    async def wrapper(*args, **kwargs) -> str:
        # Get the prompt if it exists in kwargs
        prompt = kwargs.get('prompt', '')
        
        # Check if command requires a prompt and none was provided
        if getattr(func, 'requires_prompt', False) and not prompt:
            return f"Please provide input after !{func.__name__.replace('_command', '')}"
        
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            return f"Sorry, there was an error processing your request: {str(e)}"
    return wrapper

def requires_prompt(func: Callable) -> Callable:
    """Decorator to mark commands that require a prompt."""
    func.requires_prompt = True
    return func 