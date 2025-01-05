# userapp/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from eventapp.models import Booking  # Import Booking model directly, since you're referencing it

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    address = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.username} ({self.email})"

class ChangeRequest(models.Model):
    REQUEST_TYPES = [
        ('venue', 'Venue'),
        ('date', 'Date'),
        ('other', 'Other'),
    ]
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)  # Directly refer to Booking here
    request_type = models.CharField(max_length=5, choices=REQUEST_TYPES)
    new_value = models.CharField(max_length=200)
    status = models.CharField(max_length=20, default='Pending')  # Example statuses: Pending, Approved, Rejected
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Change Request from {self.user.username} for {self.booking.event_name}"
