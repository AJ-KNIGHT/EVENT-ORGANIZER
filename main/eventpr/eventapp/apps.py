from django.apps import AppConfig


class EventappConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "eventapp"
    def ready(self):
        # Import and connect the signal
        import eventapp.signals
        
# eventapp/apps.py
from django.apps import AppConfig

class EventappConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "eventapp"

    def ready(self):
        import eventapp.signals  # This ensures that the signals are registered when the app is ready.
