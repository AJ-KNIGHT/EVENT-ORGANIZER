""" from django.db import models

class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('UPI', 'UPI'),
        ('Bank Transfer', 'Bank Transfer'),
        ('Cash', 'Cash'),
        ('Online', 'Online Payment Gateway'),
        ('Razorpay', 'Razorpay'),
    ]

    booking = models.ForeignKey(
        'eventapp.Booking', related_name='payments', on_delete=models.CASCADE
    )
    razorpay_order_id = models.CharField(max_length=255, blank=True, null=True)  # Razorpay Order ID
    razorpay_payment_id = models.CharField(max_length=255, blank=True, null=True)  # Razorpay Payment ID
    razorpay_signature = models.CharField(max_length=255, blank=True, null=True)  # Razorpay Signature

    proof_of_payment = models.ImageField(upload_to='pic/payment_proof/', blank=True, null=True)
    payment_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[('Pending', 'Pending'), ('Completed', 'Completed'), ('Verified', 'Verified')],
        default='Pending'
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    payment_method = models.CharField(
        max_length=50, choices=PAYMENT_METHOD_CHOICES, default='Razorpay'
    )

    def __str__(self):
        return f"Payment for Booking #{self.booking.id} - Status: {self.status}"

    def save(self, *args, **kwargs):
        # Logic for updating booking payment status if needed
        if self.status == 'Completed':
            self.booking.payment_status = 'Paid'
            self.booking.save()
        super().save(*args, **kwargs)
 """