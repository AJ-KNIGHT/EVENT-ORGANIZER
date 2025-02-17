import time

def timestamp(request):
    return {
        'timestamp': int(time.time())  # Or use any versioning logic you prefer
    }
# userapp/context_processors.py (or any app you prefer)

def toast_message(request):
    """
    This context processor will add the message and type to all templates.
    """
    return {
        'toast_message': {
            'type': getattr(request, 'toast_type', None),  # Default to None if not set
            'message': getattr(request, 'toast_message', None),  # Default to None if not set
        }
    }
