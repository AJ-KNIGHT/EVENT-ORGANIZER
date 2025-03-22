from django.db import models
from userapp.models import CustomUser
from eventapp.models import Booking

class Payment(models.Model):
    PAYMENT_METHODS = [
        ('COD', 'Cash on Delivery'),
        ('RAZORPAY', 'Razorpay Online Payment'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, default=None)
    booking = models.OneToOneField(
        Booking, on_delete=models.CASCADE, related_name='payment_related'  # Change the related_name here
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2)  # Stored in INR
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHODS, default='COD')
    is_paid = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=255, blank=True, null=True)  # Store Razorpay transaction ID
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment for Booking {self.booking.id} - {self.get_payment_method_display()}"

    def mark_as_paid(self, transaction_id=None):
        """
        Mark payment as completed and optionally store transaction details.
        """
        self.is_paid = True
        if transaction_id:
            self.transaction_id = transaction_id
        self.save()

    def update_payment_status(self, amount_paid):
        """
        Update the payment status based on the amount paid.
        """
        if amount_paid >= self.amount:
            self.is_paid = True
        else:
            self.is_paid = False
        self.save()
