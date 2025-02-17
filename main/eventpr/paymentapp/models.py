from django.db import models
from userapp.models import CustomUser  # Assuming you use CustomUser
from eventapp.models import Booking  # Assuming Booking is in eventapp

class Payment(models.Model):
    PAYMENT_METHODS = [
        ('COD', 'Cash on Delivery'),
        ('UPI', 'UPI (Not Available)'),
        ('NB', 'Net Banking (Not Available)'),
        ('CC', 'Credit Card (Not Available)'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, default=None)

    booking = models.OneToOneField('eventapp.Booking', on_delete=models.CASCADE, related_name='payment_booking')

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHODS, default='COD')
    is_paid = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment for Booking {self.booking.id} - {self.get_payment_method_display()}"
