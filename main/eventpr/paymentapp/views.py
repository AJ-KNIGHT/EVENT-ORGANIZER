
from django.shortcuts import render, redirect
from django.contrib import messages
from eventapp.views import Event , Booking ,Payment
from userapp.utils import send_html_email
from django.conf import settings
from datetime import date

def payment_page(request):
    """ Renders the payment options page with booking details """
    booking_data = request.session.get("booking_data")
    if not booking_data:
        request.toast_type = 'warning'  # 'error', 'warning', 'info', etc.
        request.toast_message = 'Your session expired. Please book again!'

        messages.error(request, "Your session expired. Please book again.")
        return redirect("eventapp:events")

    event = Event.objects.get(id=booking_data['event_id'])

    context = {
        "event": event,
        "booking_data": booking_data,
        
    }
    return render(request, "paymentapp/payment_options.html", context,)


def confirm_payment(request):
    """ Confirms payment and creates booking after selection """
    if request.method == "POST":
        booking_data = request.session.get("booking_data")
        if not booking_data:
            request.toast_type = 'error'  # 'error', 'warning', 'info', etc.
            request.toast_message = 'Invalid session. Please try again!'

            messages.error(request, "Invalid session. Please try again.")
            return redirect("eventapp:events")

        event = Event.objects.get(id=booking_data['event_id'])
        selected_payment_method = request.POST.get("payment_method", "COD")

        # ✅ Create Booking only AFTER payment selection
        booking = Booking.objects.create(
            user=request.user,
            event_name=event,
            event_date=event.event_date,
            cus_name=booking_data["cus_name"],
            cus_email=booking_data["cus_email"],
            venue=booking_data["venue"],
            booking_date=date.today(),  # Set the current date,
            total_amount=booking_data["total_amount"],
        )

        # ✅ Create Payment Record
        payment = Payment.objects.create(
            user=request.user,
            booking=booking,
            amount=booking.total_amount,
            payment_method=selected_payment_method,
            is_paid=False if selected_payment_method == "COD" else True
        )

        booking.payment = payment
        booking.save()

        # ✅ Send Email Confirmations (User + Admin)
        send_html_email(
            subject=f"Booking Confirmation for {event.name}",
            template_name="email/booking_confirmation_email.html",
            context={"cus_name": booking.cus_name, "event_name": event.name, "total_amount": booking.total_amount},
            recipient_list=[booking.cus_email],
        )

        send_html_email(
            subject=f"New Booking for {event.name}",
            template_name="email/new_booking_notification.html",
            context={"event_name": event.name, "cus_name": booking.cus_name, "total_amount": booking.total_amount},
            recipient_list=[settings.ADMIN_EMAIL],
        )

        # ✅ Remove session data after booking
        del request.session["booking_data"]
        request.toast_type = 'success'  # 'error', 'warning', 'info', etc.
        request.toast_message = f"Booking confirmed! Payment selected: ' { selected_payment_method}"

        messages.success(request, "Booking confirmed! Payment selected: " + selected_payment_method)

        

        return redirect("paymentapp:payment_success", )  # Redirect to success page
        
        
    return redirect("paymentapp:payment_page" , )

def payment_success(request):
    """ Payment success confirmation page """
    return render(request, 'paymentapp/payment_success.html')
