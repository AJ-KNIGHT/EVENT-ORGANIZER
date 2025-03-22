from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.core.management import call_command

@receiver(post_migrate)
def load_fixture(sender, **kwargs):
    if sender.name == 'eventapp':  # Replace with your app name
        # Load the fixture
        call_command('loaddata', 'qa_data.json')
        
# eventapp/signals.py
import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import EventCustomization, Booking

logger = logging.getLogger(__name__)

from eventapp.utils import calculate_total_price

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import EventCustomization
from .utils import calculate_total_price  # If needed

@receiver(post_save, sender=EventCustomization)
def update_booking_total(sender, instance, created, **kwargs):
    """
    Update the related Booking's total_amount whenever an EventCustomization is saved.
    """
    booking = instance.booking
    # Use the calculate_price method from EventCustomization
    new_total = instance.calculate_price()

    if booking.total_amount != new_total:
        booking.total_amount = new_total
        booking.save(update_fields=['total_amount'])
        logger.info(f"Booking {booking.id} total updated to: {booking.total_amount}")





