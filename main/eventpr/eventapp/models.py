from django.db import models, transaction
from django.utils.text import slugify
from django.utils import timezone
from django.conf import settings
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from decimal import Decimal
import logging

logger = logging.getLogger(__name__)

# Event Model
# Event Model
from django.db import models, transaction
from decimal import Decimal
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
import logging

logger = logging.getLogger(__name__)

class Event(models.Model):
    name = models.CharField(max_length=200)
    is_available = models.BooleanField(default=True)
    slug = models.SlugField(unique=True, blank=True)
    desc = models.TextField(default='No description provided')
    available_until = models.DateField(null=True, blank=True)  # New field: Book until this date
    estimated_price = models.DecimalField(
        max_digits=12, decimal_places=2, default=Decimal('0.00'),
        help_text="Starting price in INR, final price depends on customization."
    )
    img = models.ImageField(upload_to='events/', blank=True, null=True)
    event_type = models.CharField(max_length=50, default='Not specified')
    event_duration = models.CharField(max_length=50, default='Not specified')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def is_booking_allowed(self):
        from django.utils.timezone import now
        return self.is_available and (self.available_until is None or now().date() <= self.available_until)

class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings')
    event = models.ForeignKey('Event', on_delete=models.CASCADE, related_name='bookings')
    booking_date = models.DateField(auto_now_add=True)
    event_date = models.DateField()
    custom_venue = models.BooleanField(default=False)
    venue_tier = models.CharField(
        max_length=10, choices=[("Minimal", "Minimal"), ("Medium", "Medium"), ("Luxury", "Luxury")], blank=True, null=True
    )
    venue_description = models.TextField(blank=True, null=True)
    cus_name = models.CharField(max_length=255)
    cus_email = models.EmailField()
    cus_ph = models.CharField(
        max_length=10,
        validators=[RegexValidator(r'^\d{10}$', message="Phone number must be 10 digits.")]
    )
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Cancelled', 'Cancelled'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    admin_notes = models.TextField(blank=True, null=True)
    customer_request = models.TextField(blank=True, null=True)
    payment = models.OneToOneField(
        'paymentapp.Payment', on_delete=models.SET_NULL, related_name='booking_payment', null=True, blank=True)

    total_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Booking for {self.event.name} by {self.cus_name}"

    def save(self, *args, **kwargs):
        if hasattr(self, 'customization') and self.customization:
            self.total_amount = self.customization.calculate_price()
        else:
            self.total_amount = self.event.estimated_price
        super().save(*args, **kwargs)
        logger.info(f"Booking saved: {self} - Total Amount: {self.total_amount}")

from decimal import Decimal
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
import json

class EventCustomization(models.Model):
    booking = models.OneToOneField(
        Booking, on_delete=models.CASCADE, related_name="customization"
    )
    TIER_CHOICES = [
        ("Minimal", "Minimal"),
        ("Medium", "Medium"),
        ("Premium", "Premium"),
    ]
    tier = models.CharField(max_length=10, choices=TIER_CHOICES, default="Minimal")
    guest_count = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(200)],
        default=1
    )
    venue_size = models.CharField(max_length=50, blank=True, null=True)
    selected_location = models.CharField(max_length=255, blank=True, null=True)
    venue_subtier = models.CharField(max_length=100, blank=True, null=True)
    custom_venue_description = models.TextField(blank=True, null=True)
    add_ons = models.JSONField(default=dict, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="customizations")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Customization ({self.user.username} - {self.tier})"

    def calculate_price(self):
        """
        Calculate the total price for this customization.
        """
        base_price = Decimal("5000.00")
        guest_price = Decimal(self.guest_count) * Decimal("500.00")
        addon_price = sum(Decimal(opt.get("price", 0)) for opt in self.add_ons.values())

        if self.tier == "Premium":
            base_price += Decimal("2000.00")
        elif self.tier == "Medium":
            base_price += Decimal("1000.00")

        return base_price + guest_price + addon_price

    def save(self, *args, **kwargs):
        self.total_price = self.calculate_price()
        super().save(*args, **kwargs)



from django.utils.html import format_html

class EventLocation(models.Model):
    booking = models.OneToOneField(
        Booking, on_delete=models.CASCADE, related_name="location", null=True, blank=True
    )
    name = models.CharField(max_length=255, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    full_address = models.CharField(max_length=500, blank=True, null=True)
    pincode = models.CharField(max_length=20, blank=True, null=True)
    place_id = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def google_maps_link(self):
        """Returns a Google Maps link."""
        return f"https://www.google.com/maps?q={self.latitude},{self.longitude}"

    def openstreetmap_link(self):
        """Returns an OpenStreetMap link."""
        return f"https://www.openstreetmap.org/?mlat={self.latitude}&mlon={self.longitude}#map=15/{self.latitude}/{self.longitude}"

    def __str__(self):
        return self.name if self.name else f"Lat: {self.latitude}, Lon: {self.longitude}"


@transaction.atomic
def ensure_booking_integrity(sender, instance, **kwargs):
    EventLocation.objects.get_or_create(
        booking=instance,
        defaults={'latitude': 0.0, 'longitude': 0.0}  # Provide default values
    )
    EventCustomization.objects.get_or_create(booking=instance, user=instance.user)


models.signals.post_save.connect(ensure_booking_integrity, sender=Booking)

class AddOn(models.Model):
    name = models.CharField(max_length=100, unique=True)
    display_name = models.CharField(max_length=100)
    per_guest = models.BooleanField(default=False)
    options = models.JSONField()
    tiers_allowed = models.JSONField(default=list)
    image_url = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.display_name


# Contact Model
class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    submitted_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.email}"

# ChatbotQA Model
class ChatbotQA(models.Model):
    question = models.CharField(max_length=255, unique=True)
    answer = models.TextField()
    keywords = models.CharField(max_length=255, help_text="Comma-separated keywords for matching")

    def __str__(self):
        return self.question
