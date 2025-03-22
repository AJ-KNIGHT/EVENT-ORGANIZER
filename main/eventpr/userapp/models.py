# userapp/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from eventapp.models import Booking  # Import Booking model directly, since it's referenced
from django.utils import timezone
from django.conf import settings

# ---------- CUSTOM USER MODEL ----------
class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)

    def __str__(self):
        return f"{self.username} ({self.email})"


# ---------- CHANGE REQUEST MODEL ----------
class ChangeRequest(models.Model):
    REQUEST_TYPES = [
        ('Update Booking', 'Update Booking'),
        ('Reschedule Event', 'Reschedule Event'),
        ('Change Venue', 'Change Venue'),
        ('Add-ons Change', 'Add-ons Change'),
        ('Other', 'Other'),
    ]
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='change_requests'
    )
    request_type = models.CharField(max_length=100, choices=REQUEST_TYPES)
    new_value = models.TextField(help_text="Provide details about the requested change.")
    customer_request = models.TextField(
        blank=True,
        null=True,
        help_text="Optional: Additional explanation or comments."
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Change Request ({self.request_type}) by {self.user}"
