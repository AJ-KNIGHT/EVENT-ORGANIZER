from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.core.management import call_command

@receiver(post_migrate)
def load_fixture(sender, **kwargs):
    if sender.name == 'eventapp':  # Replace with your app name
        # Load the fixture
        call_command('loaddata', 'qa_data.json')