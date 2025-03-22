from django.shortcuts import render, redirect
from django.contrib import messages
from eventapp.models import Event, Booking, EventCustomization
from .models import Payment
from userapp.utils import send_html_email
from django.conf import settings
from datetime import date
from eventapp.utils import calculate_total_price
from django.contrib.auth.decorators import login_required
import logging
from django.shortcuts import render, redirect
from django.contrib import messages
from eventapp.models import Event

# Set up logger
logger = logging.getLogger(__name__)

def payment_page(request):
    """ Renders the payment options page with booking details """
    
    # Log session data before trying to fetch booking_data
    logger.debug(f"Session data at payment_page: {request.session.items()}")

    # Check for booking data in session
    booking_data = request.session.get("booking_data")

    # If booking data is not found, log the error and redirect
    if not booking_data:
        logger.error(f"Booking data is missing in session. Current session data: {request.session.items()}")
        request.toast_type = 'warning'  # 'error', 'warning', 'info', etc.
        request.toast_message = 'Your session expired. Please book again!'
        messages.error(request, "Your session expired. Please book again.")
        return redirect("eventapp:events")

    # If booking data is found, log it for verification
    logger.debug(f"Booking data found in session: {booking_data}")

    try:
        # Fetch the event associated with the booking data
        event = Event.objects.get(id=booking_data['event_id'])

        # Pass relevant context for the payment page
        context = {
            "event": event,
            "booking_data": booking_data,
            "total_amount": booking_data.get("total_amount", 0),
        }
        return render(request, "paymentapp/payment_options.html", context)
    
    except Event.DoesNotExist:
        logger.error(f"Event with ID {booking_data['event_id']} not found.")
        messages.error(request, "The event associated with this booking is no longer available.")
        return redirect("eventapp:events")


@login_required
def confirm_payment(request):
    """ Confirms payment and saves all session data to the database """
    if request.method == "POST":
        # Check if the event_slug is in the session, otherwise redirect
        if not request.session.get("event_slug"):
            messages.error(request, "Session expired. Please start over.")
            return redirect("eventapp:events")

        # Get the event based on the slug stored in session
        event = Event.objects.get(slug=request.session["event_slug"])
        selected_payment_method = request.POST.get("payment_method", "COD")  # Default to COD

        # Retrieve session data for booking and customization details
        selected_event_date = request.session.get("selected_event_date")
        selected_venue = request.session.get("selected_venue")
        customization = request.session.get("customization", {})
        total_amount = calculate_total_price(customization)
        selected_tier = request.session.get("selected_tier", "Minimal")
        venue_subtier = request.session.get("venue_subtier")
        custom_venue_description = request.session.get("custom_venue_description", "")

        # ✅ Create Booking (Final Step)
        booking = Booking.objects.create(
            user=request.user,
            event=event,
            event_date=selected_event_date,
            venue=selected_venue,
            total_amount=total_amount,
        )

        # ✅ Create Event Customization
        EventCustomization.objects.create(
            booking=booking,
            tier=selected_tier,
            selected_options=customization,
            guest_count=customization.get("guest_count", 0),
            venue_subtier=venue_subtier,
            custom_venue_description=custom_venue_description,
        )

        # ✅ Create Payment record
        Payment.objects.create(
            user=request.user,
            booking=booking,
            amount=total_amount,
            payment_method=selected_payment_method,
            is_paid=False if selected_payment_method == "COD" else True
        )

        # ✅ Clear session after saving the data
        request.session.flush()
        
        # Inform the user that the booking was confirmed
        messages.success(request, "Booking confirmed!")
        return redirect("paymentapp:payment_success")

    # If it's not a POST request, redirect to the payment page
    return redirect("paymentapp:payment_page")


def payment_success(request):
    """ Payment success confirmation page """
    # Simply render the success page after payment confirmation
    return render(request, 'paymentapp/payment_success.html')
