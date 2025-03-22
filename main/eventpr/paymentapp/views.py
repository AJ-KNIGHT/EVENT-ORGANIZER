
from django.shortcuts import render, redirect
from django.contrib import messages
from eventapp.views import Event , Booking ,Payment
from userapp.utils import send_html_email
from django.conf import settings
from datetime import date
from eventapp.utils import calculate_total_price
from django.contrib.auth.decorators import login_required

def payment_page(request):
    """ Renders the payment options page with booking details """
    booking_data = request.session.get("booking_data")
    if not booking_data:
        print("Session expired or booking data missing!")  # Add debug log
        request.toast_type = 'warning'  # 'error', 'warning', 'info', etc.
        request.toast_message = 'Your session expired. Please book again!'
        messages.error(request, "Your session expired. Please book again.")
        return redirect("eventapp:events")

    event = Event.objects.get(id=booking_data['event_id'])

    context = {
        "event": event,
        "booking_data": booking_data,
    }
    return render(request, "paymentapp/payment_options.html", context)


@login_required
def confirm_payment(request):
    """ Confirms payment and saves all session data to database """
    if request.method == "POST":
        if not request.session.get("event_slug"):
            messages.error(request, "Session expired. Please start over.")
            return redirect("eventapp:events")

        event = Event.objects.get(slug=request.session["event_slug"])
        selected_payment_method = request.POST.get("payment_method", "COD")

        # ✅ Create Booking (Final Step)
        booking = Booking.objects.create(
            user=request.user,
            event=event,
            event_date=request.session.get("selected_event_date"),
            venue=request.session.get("selected_venue"),
            total_amount=calculate_total_price(request.session.get("customization", {})),
        )

        # ✅ Create Event Customization
        EventCustomization.objects.create(
            booking=booking,
            tier=request.session.get("selected_tier", "Minimal"),
            selected_options=request.session.get("customization", {}),
            guest_count=request.session.get("customization", {}).get("guest_count", 0),
            venue_subtier=request.session.get("venue_subtier"),
            custom_venue_description=request.session.get("custom_venue_description", ""),
        )

        # ✅ Create Payment
        Payment.objects.create(
            user=request.user,
            booking=booking,
            amount=booking.total_amount,
            payment_method=selected_payment_method,
            is_paid=False if selected_payment_method == "COD" else True
        )

        # ✅ Clear session after saving
        request.session.flush()
        messages.success(request, "Booking confirmed!")
        return redirect("paymentapp:payment_success")

    return redirect("paymentapp:payment_page")




def payment_success(request):
    """ Payment success confirmation page """
    return render(request, 'paymentapp/payment_success.html')
