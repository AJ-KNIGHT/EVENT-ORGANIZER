from django.db import models
from django.utils.text import slugify
from django.conf import settings
from django.core.validators import RegexValidator
from decimal import Decimal
from django.db import models
from eventapp.models import Event

# ✅ Define Event first, since other models depend on it
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

    def __str__(self):
        return self.name


# ✅ Now Booking can safely reference Event


class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='bookings')
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
        customization, _ = EventCustomization.objects.get_or_create(booking=self)
        self.total_amount = customization.calculate_price()
        super().save(*args, **kwargs)


class EventCustomization(models.Model):
    TIER_CHOICES = [("Minimal", "Minimal"), ("Medium", "Medium"), ("Premium", "Premium")]

    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name="customization")
    tier = models.CharField(max_length=10, choices=TIER_CHOICES, default="Minimal")
    guest_count = models.PositiveIntegerField(default=1)

    selected_location = models.CharField(max_length=255, blank=True, null=True, default="")
    def __str__(self):
        return f"Customization for {self.booking.event.name} - Location: {self.selected_location}"

    venue_size = models.CharField(
        max_length=10,
        choices=[("Small", "Small"), ("Medium", "Medium"), ("Large", "Large")],
        default="Small",
        blank=True,
        null=True
    )

    catering = models.CharField(max_length=20, choices=[
        ("Standard", "Standard"), ("Buffet", "Buffet"),
        ("Multi-Course", "Multi-Course"), ("Custom", "Custom Menu")
    ], default="Standard")

    decorations = models.CharField(max_length=20, choices=[
        ("Basic", "Basic"), ("Themed", "Themed"), ("Luxury", "Luxury")
    ], default="Basic")

    entertainment = models.CharField(max_length=20, choices=[
        ("None", "None"), ("DJ", "DJ"), ("Live Band", "Live Band"), ("Projector", "Projector")
    ], default="None")

    seating_arrangement = models.CharField(max_length=10, choices=[
        ("Formal", "Formal"), ("Casual", "Casual"), ("Custom", "Custom")
    ], default="Formal")

    photography = models.CharField(max_length=20, choices=[
        ("None", "None"), ("Basic", "Basic"), ("Professional", "Professional")
    ], default="None")

    lighting_effects = models.CharField(max_length=20, choices=[
        ("Basic", "Basic"), ("Themed", "Themed"), ("Premium", "Premium")
    ], default="Basic")

    # New Fields
    audio_visual = models.BooleanField(default=False)
    medical_support = models.BooleanField(default=False)
    event_manager = models.BooleanField(default=False)
    post_event_media = models.BooleanField(default=False)
    cleanup_service = models.BooleanField(default=False)

    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def calculate_price(self):
        base_price = self.booking.event.price or Decimal('0.00')
        tier_pricing = {"Minimal": 0, "Medium": 500, "Premium": 1000}
        base_price += Decimal(tier_pricing[self.tier])

        add_ons = {
            "catering": {"Standard": 0, "Buffet": 300, "Multi-Course": 600, "Custom": 800},
            "decorations": {"Basic": 0, "Themed": 400, "Luxury": 1000},
            "entertainment": {"None": 0, "DJ": 300, "Live Band": 700, "Projector": 500},
            "photography": {"None": 0, "Basic": 400, "Professional": 1000},
            "lighting_effects": {"Basic": 0, "Themed": 300, "Premium": 700},
        }

        if not self.booking.custom_venue:
            add_ons["venue_size"] = {"Small": 0, "Medium": 500, "Large": 1000}

        extra_cost = sum(add_ons[field][getattr(self, field)] for field in add_ons if hasattr(self, field))

        # New Feature Prices
        extra_cost += 500 if self.audio_visual else 0
        extra_cost += 300 if self.medical_support else 0
        extra_cost += 700 if self.event_manager else 0
        extra_cost += 400 if self.post_event_media else 0
        extra_cost += 600 if self.cleanup_service else 0

        return base_price + extra_cost

    def save(self, *args, **kwargs):
        self.total_price = self.calculate_price()
        super().save(*args, **kwargs)



class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    submitted_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.email}"


class ChatbotQA(models.Model):
    question = models.CharField(max_length=255, unique=True)
    answer = models.TextField()
    keywords = models.CharField(max_length=255, help_text="Comma-separated keywords for matching")

    def __str__(self):
        return self.question
