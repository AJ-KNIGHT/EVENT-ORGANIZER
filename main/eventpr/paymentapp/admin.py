from django.contrib import admin
from .models import Payment

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('booking', 'proof_of_payment', 'payment_date', 'status', 'payment_method', 'razorpay_payment_id')
    search_fields = ('booking__id', 'booking__user__username', 'status', 'razorpay_payment_id')  # Search by booking ID, username, status, and Razorpay payment ID
    list_filter = ('status', 'payment_date', 'payment_method')  # Filter by payment status, payment date, and payment method
    readonly_fields = ('booking', 'proof_of_payment', 'payment_date', 'razorpay_payment_id', 'razorpay_signature')  # Make Razorpay fields read-only for admins

    # Optional: Add the ability to change payment status directly in the admin
    actions = ['mark_as_completed', 'mark_as_verified']

    def mark_as_completed(self, request, queryset):
        queryset.update(status='Completed')
        for payment in queryset:
            # Also update the related booking's payment status
            payment.booking.payment_status = 'Paid'
            payment.booking.save()
        self.message_user(request, "Selected payments marked as completed.")
    mark_as_completed.short_description = "Mark selected payments as completed"

    def mark_as_verified(self, request, queryset):
        queryset.update(status='Verified')
        for payment in queryset:
            # Update booking status if necessary
            payment.booking.payment_status = 'Verified'
            payment.booking.save()
        self.message_user(request, "Selected payments marked as verified.")
    mark_as_verified.short_description = "Mark selected payments as verified"

# Register the Payment model with the custom admin
admin.site.register(Payment, PaymentAdmin)
