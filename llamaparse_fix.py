"""
Compatibility fix for llama-parse with newer pydantic versions.
This module provides a monkey patch to make older llama-parse versions work with newer pydantic.
"""

def fix_llamaparse_compatibility():
    """
    Monkey patch to fix compatibility between older llama-parse and newer pydantic versions.
    """
    try:
        # Import the bridge module
        from llama_index.core.bridge import pydantic as bridge_pydantic
        from functools import wraps
        
        # Check if validator is missing but field_validator exists
        if not hasattr(bridge_pydantic, 'validator') and hasattr(bridge_pydantic, 'field_validator'):
            # Create a compatibility wrapper that adapts old validator syntax to new field_validator
            def validator_wrapper(*fields, pre=False, always=False, **kwargs):
                """Wrapper to make old validator syntax work with new field_validator"""
                def decorator(func):
                    # Convert old parameters to new field_validator format
                    mode = 'before' if pre else 'after'
                    return bridge_pydantic.field_validator(*fields, mode=mode)(func)
                return decorator
            
            # Apply the wrapper
            bridge_pydantic.validator = validator_wrapper
            print("✅ Applied llama-parse compatibility fix")
        
    except ImportError:
        print("⚠️ Could not apply llama-parse compatibility fix")

# Apply the fix when this module is imported
fix_llamaparse_compatibility()
