from inspect import signature, Parameter
import asyncio
from functools import wraps

async def resolve_dependency(dependency):
    """
    Recursively resolves a dependency, handling both Depends instances and callable dependencies.
    """
    # Check if it's a Depends instance (without using isinstance)
    if hasattr(dependency, 'dependency') and hasattr(dependency, 'use_cache'):
        # This is the safest way to identify a Depends instance
        dependency = dependency.dependency
    
    if callable(dependency):
        # Get the function signature
        sig = signature(dependency)
        
        # Prepare arguments
        kwargs = {}
        for name, param in sig.parameters.items():
            # Handle parameters with Depends defaults
            param_default = param.default
            if hasattr(param_default, 'dependency') and hasattr(param_default, 'use_cache'):
                kwargs[name] = await resolve_dependency(param_default)
            # Handle parameters with no defaults but type annotations
            elif param.default is Parameter.empty and param.annotation is not Parameter.empty:
                # You might want to add special cases here if needed
                pass
        
        # Call the dependency with resolved arguments
        result = dependency(**kwargs)
        if asyncio.iscoroutine(result):
            result = await result
        return result
    
    # If it's not callable and not a Depends, return as-is
    return dependency