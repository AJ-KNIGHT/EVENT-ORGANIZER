""" import razorpay
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.http import JsonResponse

from .forms import PaymentForm
from .models import Payment
from eventapp.models import Booking

# Initialize Razorpay client with your Razorpay key and secret from settings
razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

@login_required
def payment_view(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    
    # Initialize payment details
    payment_method = None
    razorpay_order_id = None

    # Process payment options
    if request.method == 'POST':
        form = PaymentForm(request.POST, request.FILES)
        
        if form.is_valid():
            payment = form.save(commit=False)
            payment.booking = booking
            payment.amount = booking.total_amount

            # Get the payment method from the form
            payment_method = form.cleaned_data['payment_method']
            booking.payment_method = payment_method

            # Handle the logic for each payment method
            if payment_method == 'Cash':
                booking.payment_status = 'Pending'  # Cash will be paid later
                payment.save()  # Cash doesn't need to be processed immediately
            else:
                payment.save()  # For UPI, Bank Transfer, and Online (Razorpay)
                booking.payment_status = 'Pending'  # Set status to pending for now
            
            booking.save()

            # Notify the admin
            send_mail(
                subject="New Payment Submitted",
                message=f"Payment for Booking #{booking.id} has been submitted.\nPayment Method: {payment_method}\nAmount: ₹{payment.amount}.",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[settings.ADMIN_EMAIL],
            )

            messages.success(request, "Payment information submitted successfully.")
            return redirect('eventapp:booking_dashboard')
    else:
        form = PaymentForm()

    # Generate Razorpay order if the payment method is Online
    if booking.payment_method == 'Online':
        razorpay_order_id = create_razorpay_order(booking.total_amount)
        # Create a Payment record for Razorpay with status 'Pending'
        payment = Payment.objects.create(
            booking=booking,
            amount=booking.total_amount,
            payment_method='Online',
            status='Pending',
            razorpay_order_id=razorpay_order_id
        )

    return render(request, 'payment.html', {
        'booking': booking,
        'form': form,
        'razorpay_order_id': razorpay_order_id,
        'razorpay_key_id': settings.RAZORPAY_KEY_ID,  # Razorpay key ID for frontend integration
        'payment_method': payment_method,
    })

def create_razorpay_order(amount):
   
    Create a Razorpay order with the specified amount.
    Amount is expected to be in INR (paise), so we multiply by 100.

    amount_in_paise = int(amount * 100)  # Convert to paise
    order = razorpay_client.order.create(dict(
        amount=amount_in_paise,  # Amount in paise
        currency='INR',
        receipt=str(order['id']),  # Unique receipt identifier
        notes={'description': 'Event Booking Payment'}
    ))
    return order['id']

@login_required
def payment_verify(request):
 
    Verify Razorpay payment after the user completes the transaction.
    This method will handle the verification of the payment signature and status.
 
    if request.method == 'POST':
        data = request.body.decode('utf-8')
        payment_data = json.loads(data)

        razorpay_order_id = payment_data.get('razorpay_order_id')
        razorpay_payment_id = payment_data.get('razorpay_payment_id')
        razorpay_signature = payment_data.get('razorpay_signature')

        # Verify the signature using Razorpay's helper method
        try:
            response = razorpay_client.utility.verify_payment_signature({
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': razorpay_payment_id,
                'razorpay_signature': razorpay_signature
            })
            
            if response is None:
                raise ValueError("Invalid Signature")

            # Mark the payment as completed
            payment = Payment.objects.get(razorpay_order_id=razorpay_order_id)
            payment.status = 'Completed'
            payment.razorpay_payment_id = razorpay_payment_id
            payment.save()

            # Update booking payment status
            booking = payment.booking
            booking.payment_status = 'Paid'
            booking.save()

            # Notify the admin about the successful payment
            send_mail(
                subject="Payment Completed",
                message=f"Payment for Booking #{booking.id} has been completed successfully using Razorpay.\nAmount: ₹{booking.total_amount}.",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[settings.ADMIN_EMAIL],
            )

            return JsonResponse({"status": "success", "message": "Payment verified"})
        except Exception as e:
            return JsonResponse({"status": "failure", "message": str(e)})

    return JsonResponse({"status": "failure", "message": "Invalid request"})
 """