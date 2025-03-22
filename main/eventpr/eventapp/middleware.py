import logging

logger = logging.getLogger(__name__)

class SessionLoggerMiddleware:
    """Middleware to log session data for debugging."""
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Log session data before processing the request
        if request.user.is_authenticated:
            logger.info(f"Session Data for {request.user}: {request.session.items()}")

        response = self.get_response(request)

        return response
