from django.db import models
from django.utils.text import slugify
from django.conf import settings
from decimal import Decimal
from django.utils import timezone

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

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.get_unique_slug(slugify(self.name))
        super().save(*args, **kwargs)

    def get_unique_slug(self, slug):
        original_slug = slug
        counter = 1
        while Event.objects.filter(slug=slug).exists():
            slug = f"{original_slug}-{counter}"
            counter += 1
        return slug

    def __str__(self):
        return self.name


# eventapp/models.py
class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings')
    event_name =  models.ForeignKey(Event, on_delete=models.CASCADE, related_name='bookings')
    event_date = models.DateField()
    venue = models.CharField(max_length=255)
    booking_date = models.DateField()
    admin_notes = models.TextField(blank=True, null=True)
    customer_request = models.TextField(blank=True, null=True)
    cus_name = models.CharField(max_length=255)
    cus_email = models.EmailField()
    cus_ph = models.CharField(max_length=10)
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"Booking for {self.event_name} by {self.cus_name}"




class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    submitted_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.email}"



