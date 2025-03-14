# userapp/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from eventapp.models import Booking  # Import Booking model directly, since you're referencing it

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)  # New field

    def __str__(self):
        return f"{self.username} ({self.email})"


class ChangeRequest(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    booking = models.ForeignKey('eventapp.Booking', on_delete=models.CASCADE)  # Use a string reference
    request_type = models.CharField(
        max_length=50,
        choices=[('Date', 'Date'), ('Venue', 'Venue')]
    )  # What change is requested
    new_value = models.CharField(max_length=255)  # The new date/venue requested
    status = models.CharField(
        max_length=50,
        choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')],
        default='Pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)

