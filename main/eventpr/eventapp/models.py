from django.db import models
from django.utils.text import slugify
from django.conf import settings
from django.core.validators import RegexValidator
from decimal import Decimal
import json


# Event Model
class Event(models.Model):
    name = models.CharField(max_length=200)
    is_available = models.BooleanField(default=True)
    slug = models.SlugField(unique=True, blank=True)
    desc = models.TextField(default='no description provided')
    event_date = models.DateField()
    location = models.CharField(max_length=200, default='not specified')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    img = models.ImageField(upload_to='events/', blank=True, null=True)
    event_type = models.CharField(max_length=50, default='not specified')
    event_duration = models.CharField(max_length=50, default='not specified')
    itinerary = models.JSONField(default=list)

    def get_unique_slug(self, base_slug):
        slug = base_slug
        counter = 1
        while Event.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        return slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.get_unique_slug(slugify(self.name))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

from decimal import Decimal
from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator

# Assuming Event is defined elsewhere in your project
# from your_app.models import Event


class Booking(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings'
    )
    event = models.ForeignKey(
        'Event', on_delete=models.CASCADE, related_name='bookings'
    )
    event_date = models.DateField()
    custom_venue = models.BooleanField(default=False)
    venue = models.CharField(max_length=255, blank=True, null=True)
    booking_date = models.DateField(auto_now_add=True)
    admin_notes = models.TextField(blank=True, null=True)
    customer_request = models.TextField(blank=True, null=True)
    cus_name = models.CharField(max_length=255)
    cus_email = models.EmailField()
    cus_ph = models.CharField(
        max_length=10,
        validators=[RegexValidator(r'^\d{10}$', message="Phone number must be 10 digits.")],
    )
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Cancelled', 'Cancelled'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    description = models.TextField(blank=True, null=True)
    payment = models.OneToOneField(
        'paymentapp.Payment',
        on_delete=models.CASCADE,
        related_name='booking_payment',
        null=True, blank=True, default=None
    )
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"Booking for {self.event.name} by {self.cus_name}"

    def save(self, *args, **kwargs):
        # First, save the Booking instance to ensure it has a primary key.
        super().save(*args, **kwargs)
        # Now, get or create the related EventCustomization.
        customization, created = EventCustomization.objects.get_or_create(booking=self)
        # Update the total_amount based on the customization's calculated price.
        self.total_amount = customization.calculate_price()
        # Save again, updating only the total_amount field.
        super().save(update_fields=['total_amount'])


class AddOn(models.Model):
    name = models.CharField(max_length=100, unique=True)  # e.g. "catering"
    display_name = models.CharField(max_length=100)         # e.g. "Catering"
    is_per_guest = models.BooleanField(default=False)       # If true, cost is multiplied by guest count
    # Options stored as: { "Standard": {"Minimal": 10, "Medium": 15, "Premium": 20}, ... }
    options = models.JSONField()
    # List of tier names allowed for this addon.
    tiers_allowed = models.JSONField(default=list)

    def __str__(self):
        return self.display_name


from decimal import Decimal
import json
from django.db import models

class EventCustomization(models.Model):
    """
    Stores user customization details for an event, including tier, guest count,
    addon selections, extra sub‑options, and the computed total price.
    """
    TIER_CHOICES = [
        ("Minimal", "Minimal"),
        ("Medium", "Medium"),
        ("Premium", "Premium"),
    ]

    booking = models.OneToOneField(
        'Booking', on_delete=models.CASCADE, related_name="customization"
    )
    tier = models.CharField(max_length=10, choices=TIER_CHOICES, default="Minimal")
    guest_count = models.PositiveIntegerField(default=1)

    # Store base addon selections (the chosen option for each base field)
    selected_options = models.JSONField(default=dict)
    selected_location = models.CharField(max_length=255, blank=True, null=True, default="")

    # Base event configuration fields.
    venue_size = models.CharField(
        max_length=10,
        choices=[("Small", "Small"), ("Medium", "Medium"), ("Large", "Large")],
        default="Small",
        blank=True,
        null=True
    )
    catering = models.CharField(
        max_length=20,
        choices=[
            ("None", "None"),
            ("Standard", "Standard"),
            ("Buffet", "Buffet"),
            ("Multi-Course", "Multi-Course"),
            ("Custom", "Custom Menu")
        ],
        default="None",
        blank=True,
        null=True
    )
    decorations = models.CharField(
        max_length=20,
        choices=[
            ("None", "None"),
            ("Basic", "Basic"),
            ("Themed", "Themed"),
            ("Luxury", "Luxury")
        ],
        default="None",
        blank=True,
        null=True
    )
    entertainment = models.CharField(
        max_length=20,
        choices=[
            ("None", "None"),
            ("DJ", "DJ"),
            ("Live Band", "Live Band"),
            ("Projector", "Projector")
        ],
        default="None",
        blank=True,
        null=True
    )
    seating_arrangement = models.CharField(
        max_length=20,
        choices=[
            ("None", "None"),
            ("Formal", "Formal"),
            ("Casual", "Casual"),
            ("Custom", "Custom")
        ],
        default="None",
        blank=True,
        null=True
    )
    table_arrangements = models.CharField(
        max_length=20,
        choices=[
            ("None", "None"),
            ("Basic", "Basic"),
            ("Themed", "Themed"),
            ("Premium", "Premium")
        ],
        default="None",
        blank=True,
        null=True
    )
    photography = models.CharField(
        max_length=20,
        choices=[
            ("None", "None"),
            ("Basic", "Basic"),
            ("Professional", "Professional")
        ],
        default="None",
        blank=True,
        null=True
    )
    lighting_effects = models.CharField(
        max_length=20,
        choices=[
            ("None", "None"),
            ("Basic", "Basic"),
            ("Themed", "Themed"),
            ("Premium", "Premium")
        ],
        default="None",
        blank=True,
        null=True
    )

    # Additional Boolean addons.
    audio_visual = models.BooleanField(default=False)
    medical_support = models.BooleanField(default=False)
    event_manager = models.BooleanField(default=False)
    cleanup_service = models.BooleanField(default=False)

    # Extra sub‑options for addons (e.g., {"catering": {"veg": true, "cuisine": "Italian"}, ...})
    addon_details = models.JSONField(default=dict, blank=True, null=True)

    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))

    def calculate_price(self):
        # Start with the event's base price.
        base_price = self.booking.event.price or Decimal('0.00')
        tier_pricing = {"Minimal": Decimal('0'), "Medium": Decimal('500'), "Premium": Decimal('1000')}
        base_price += tier_pricing.get(self.tier, Decimal('0'))
        total = base_price

        from .models import AddOn

        addon_fields = {
            'catering': self.catering,
            'decorations': self.decorations,
            'entertainment': self.entertainment,
            'photography': self.photography,
            'lighting_effects': self.lighting_effects,
        }

        for field, selected_option in addon_fields.items():
            if selected_option and selected_option != 'None':
                try:
                    addon = AddOn.objects.get(name=field)
                    # Ensure addon.options is a dictionary.
                    if isinstance(addon.options, str):
                        options_dict = json.loads(addon.options)
                    else:
                        options_dict = addon.options
                    price_dict = options_dict.get(selected_option, {})
                    price = price_dict.get(self.tier)
                    if price is not None:
                        price = Decimal(str(price))
                        if addon.is_per_guest:
                            total += price * self.guest_count
                        else:
                            total += price
                except AddOn.DoesNotExist:
                    continue

        # Additional Boolean addons.
        total += Decimal('500') if self.audio_visual else Decimal('0')
        total += Decimal('300') if self.medical_support else Decimal('0')
        total += Decimal('700') if self.event_manager else Decimal('0')
        total += Decimal('600') if self.cleanup_service else Decimal('0')

        # Process extra costs from addon_details (e.g., sub-options for catering).
        details = self.addon_details or {}
        catering_details = details.get("catering", {})
        cuisine = catering_details.get("cuisine")
        if self.tier == "Premium" and cuisine == "Italian":
            total += Decimal("200")

        return total

    def save(self, *args, **kwargs):
        self.total_price = self.calculate_price()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Customization for Booking {self.booking.id} ({self.tier})"



# Venue Model
class Venue(models.Model):
    name = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.name


# EventLocation Model

# EventLocation Model with linkage to Booking
class EventLocation(models.Model):
    booking = models.OneToOneField(
        Booking, on_delete=models.CASCADE, related_name="location", null=True, blank=True
    )
    name = models.CharField(max_length=255, blank=True)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.name if self.name else f"Lat: {self.latitude}, Lon: {self.longitude}"



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