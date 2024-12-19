from django.db import models
from django.utils import timezone
from django.utils.text import slugify
import uuid
from decimal import Decimal

class Event(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)  # Automatically generate unique slug
    desc = models.TextField(default='no description provided')
    event_date = models.DateField(default=timezone.now)
    location = models.CharField(max_length=200, default='not specified')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    img = models.ImageField(upload_to='events/', blank=True, null=True)
    event_type = models.CharField(max_length=50, default='not specified')
    event_duration = models.CharField(max_length=50, default='not specified')
    itinerary = models.JSONField(default=list)

    def save(self, *args, **kwargs):
    # Auto-generate slug using event name if not provided
        if not self.slug:
            self.slug = slugify(self.name)
            # Ensure uniqueness
            self.slug = self.get_unique_slug(self.slug)
        super().save(*args, **kwargs)


    def get_unique_slug(self, slug):
        """
        Generates a unique slug by appending a counter if the slug already exists.
        """
        original_slug = slug
        counter = 1
        while Event.objects.filter(slug=slug).exists():
            slug = f"{original_slug}-{counter}"
            counter += 1
        return slug

    def __str__(self):
        return self.name

class Booking(models.Model):
    cus_name = models.CharField(max_length=55)  # Customer Name
    cus_ph = models.CharField(max_length=12)  # Customer Phone
    event_name = models.CharField(max_length=100, blank=False, null=False)  # Event Name
    event_date = models.DateField()  # Event Date
    venue = models.CharField(max_length=255, blank=False, null=False)  # Venue
    description = models.TextField(blank=False, null=False)  # Event Description
    booking_date = models.DateField(auto_now=True)  # Automatically set booking date

    def __str__(self):
        return f"{self.event_name} booked by {self.cus_name}"

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    submitted_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.email}"
