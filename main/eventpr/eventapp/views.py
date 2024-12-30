from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Event, Booking , Contact
from datetime import date
from .forms import BookingForm ,ChangeRequestForm 
from django.utils.timezone import now
from django.core.mail import send_mail
from django.conf import settings
from django.core.paginator import Paginator
#from paymentapp.models import Payment
import random
from django.contrib.auth.decorators import login_required

# Index view
def index(request):
    events = Event.objects.filter(event_date__gte=now().date(), is_available=True)
    if len(events) < 3:
        random_events = events  # Display all available events if fewer than 3 exist
    else:
        random_events = random.sample(list(events), 3)
    return render(request, 'index.html', {'events': random_events})

# About view
def about(request):
    return render(request, 'about.html')

# Event list view (for pagination)
def event_list(request):
    events = Event.objects.filter(event_date__gte=now().date(), is_available=True).order_by('event_date')  # Order by event date
    paginator = Paginator(events, 6)  # Adjust the number of events per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'events.html', {'page_obj': page_obj})

# Event detail view
def event_detail(request, slug):
    event = get_object_or_404(Event, slug=slug)
    related_events = Event.objects.filter(event_type=event.event_type).exclude(id=event.id)[:3]
    return render(request, 'event_details.html', {'event': event, 'related_events': related_events})

# Booking view

""" def booking(request, slug=None):
    event = get_object_or_404(Event, slug=slug)

    # Check if the event is bookable (event date and availability)
    if event.event_date < date.today() or not event.is_available:
        messages.error(request, "Sorry, this event is not available for booking yet.")
        return redirect('events')

    # Handle both GET and POST requests
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            # Create the Booking instance without saving to the database yet
            booking = form.save(commit=False)

            # Assign the logged-in user to the booking
            booking.user = request.user  # This links the booking to the currently logged-in user

            # Save the booking to the database
            booking.save()

            # Create the Payment record associated with the Booking instance
            Payment.objects.create(
                booking=booking,  # Associate payment with the booking
                amount=0.0,  # Initial amount set to 0, updated after negotiation
                status='Pending',  # Default payment status
                # transaction_id=''  # To be updated after payment completion
            )

            # Send email notification to the user (Booking confirmation)
            subject = f"Booking Confirmation for {event.name}"
            message = f"Thank you for booking {event.name}.\nEvent Date: {event.event_date}\nVenue: {booking.venue}\n\nYour booking has been confirmed."
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [booking.cus_email],  # Use the customer's email from the form
                fail_silently=False,
            )

            # Also notify the admin
            admin_subject = f"New Booking for {event.name}"
            admin_message = f"A new booking has been made for {event.name} by {booking.cus_name}. Event Date: {event.event_date}, Venue: {booking.venue}."
            send_mail(
                admin_subject,
                admin_message,
                settings.EMAIL_HOST_USER,
                [settings.ADMIN_EMAIL],  # Admin's email from settings
                fail_silently=False,
            )

            messages.success(request, "Your event has been booked successfully! A confirmation email has been sent.")
            return redirect('event_list')
        else:
            print(f"Form Errors: {form.errors}")  # Debug line to check form errors
            messages.error(request, "There was an error with your booking. Please check the form and try again.")
    else:
        # Pre-populate the form with the event data
        initial_data = {
            'event_name': event.name,  # Ensure event_name is passed to the form
            'event_date': event.event_date,
            'venue': event.location
        }
        form = BookingForm(initial=initial_data)

    return render(request, 'booking.html', {'form': form, 'event': event}) """
# before removing the payment view |
   #                               v

""" from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Event
from .forms import BookingForm
from django.core.mail import send_mail
from django.conf import settings
from datetime import date

def booking(request, slug=None):
    event = get_object_or_404(Event, slug=slug)

    # Check if the event is bookable (event date and availability)
    if event.event_date < date.today() or not event.is_available:
        messages.error(request, "Sorry, this event is not available for booking yet.")
        return redirect('events')

    # Handle both GET and POST requests
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            # Create the Booking instance without saving to the database yet
            booking = form.save(commit=False)

            # Assign the logged-in user to the booking
            booking.user = request.user  # This links the booking to the currently logged-in user

            # Set the total amount based on the event's price
            booking.total_amount = event.price  # Set the total amount dynamically from the event's price

            # Save the booking to the database
            booking.save()

            # Send email notification to the user (Booking confirmation)
            subject = f"Booking Confirmation for {event.name}"
            message = f"Thank you for booking {event.name}.\nEvent Date: {event.event_date}\nVenue: {booking.venue}\n\nYour booking has been confirmed."
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [booking.cus_email],  # Use the customer's email from the form
                fail_silently=False,
            )

            # Also notify the admin
            admin_subject = f"New Booking for {event.name}"
            admin_message = f"A new booking has been made for {event.name} by {booking.cus_name}. Event Date: {event.event_date}, Venue: {booking.venue}."
            send_mail(
                admin_subject,
                admin_message,
                settings.EMAIL_HOST_USER,
                [settings.ADMIN_EMAIL],  # Admin's email from settings
                fail_silently=False,
            )

            # Redirect to the payment page with the booking ID
            messages.success(request, "Your event has been booked successfully! Please proceed with the payment.")
            return redirect('paymentapp:payment_view', booking_id=booking.id)
        else:
            print(f"Form Errors: {form.errors}")  # Debug line to check form errors
            messages.error(request, "There was an error with your booking. Please check the form and try again.")
    else:
        # Pre-populate the form with the event data
        initial_data = {
            'event_name': event.name,  # Ensure event_name is passed to the form
            'event_date': event.event_date,
            'venue': event.location
        }
        form = BookingForm(initial=initial_data)

    return render(request, 'booking.html', {'form': form, 'event': event}) """


def booking(request, slug=None):
    event = get_object_or_404(Event, slug=slug)

    # Check if the event is bookable (event date and availability)
    if event.event_date < date.today() or not event.is_available:
        messages.error(request, "Sorry, this event is not available for booking yet.")
        return redirect('events')

    # Handle both GET and POST requests
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            # Create the Booking instance without saving to the database yet
            booking = form.save(commit=False)

            # Assign the logged-in user to the booking
            booking.user = request.user  # This links the booking to the currently logged-in user

             # Set the event's date (admin uploaded) to the booking's event_date field
            booking.event_date = event.event_date  # Ensure event_date is set to the admin-uploaded date


            # Set the total amount based on the event's price
            booking.total_amount = event.price  # Set the total amount dynamically from the event's price

            # Save the booking to the database
            booking.save()

            # Send email notification to the user (Booking confirmation)
            subject = f"Booking Confirmation for {event.name}"
            message = f"Thank you for booking {event.name}.\nEvent Date: {event.event_date}\nVenue: {booking.venue}\n\nYour booking has been confirmed."
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [booking.cus_email],  # Use the customer's email from the form
                fail_silently=False,
            )

            # Also notify the admin
            admin_subject = f"New Booking for {event.name}"
            admin_message = f"A new booking has been made for {event.name} by {booking.cus_name}. Event Date: {event.event_date}, Venue: {booking.venue}."
            send_mail(
                admin_subject,
                admin_message,
                settings.EMAIL_HOST_USER,
                [settings.ADMIN_EMAIL],  # Admin's email from settings
                fail_silently=False,
            )

            # Commenting out the payment-related redirect
            # Redirect to the payment page with the booking ID
            # messages.success(request, "Your event has been booked successfully! Please proceed with the payment.")
            # return redirect('paymentapp:payment_view', booking_id=booking.id)

            # Instead of redirecting to the payment page, simply show a success message
            messages.success(request, "Your event has been booked successfully!")
            return redirect('events')  # Redirect to the events page or any other page you prefer
        else:
            print(f"Form Errors: {form.errors}")  # Debug line to check form errors
            messages.error(request, "There was an error with your booking. Please check the form and try again.")
    else:
        # Pre-populate the form with the event data
        initial_data = {
            'event_name': event.name,  # Ensure event_name is passed to the form
            'event_date': event.event_date,
            'venue': event.location,
            'booking_date':date.today(),
        }
        form = BookingForm(initial=initial_data)

    return render(request, 'booking.html', {'form': form, 'event': event})


# Contact view
def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        Contact.objects.create(name=name, email=email, message=message)
        messages.success(request, 'Thank you for reaching out! We will get back to you soon.')
        return redirect('contact')
    return render(request, 'contact.html')






# Change Request View
@login_required
def change_request_view(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    if request.method == 'POST':
        form = ChangeRequestForm(request.POST)
        if form.is_valid():
            booking.customer_request = form.cleaned_data['customer_request']
            booking.save()

            # Notify admin
            send_mail(
                subject="Change Request Submitted",
                message=f"A change request has been submitted for booking {booking.id}: {booking.customer_request}",
                from_email='eventpro49@gmail.com',
                recipient_list=['amal183626@gmail.com']
            )

            messages.success(request, "Change request submitted successfully.")
            return redirect('booking_dashboard')
    else:
        form = ChangeRequestForm()

    return render(request, 'change_request.html', {'booking': booking, 'form': form})

# Admin Dashboard for Review
@login_required
def admin_dashboard(request):
    if not request.user.is_staff:
        return redirect('booking_dashboard')

    bookings = Booking.objects.all()
    return render(request, 'admin_dashboard.html', {'bookings': bookings})


# Customer Booking Dashboard

@login_required  # Ensure only logged-in users can access this view
def booking_dashboard(request):
    # Fetch the user (based on logged-in user or a specific one)
    user = request.user  # Or CustomUser.objects.get(username='akash')

    # Get all bookings for the user
    user_bookings = Booking.objects.filter(user=user)

    # Render the dashboard template with the bookings
    return render(request, 'booking_dashboard.html', {'user_bookings': user_bookings})




def privacy_policy(request):
    return render(request, 'privacy_policy.html')
def terms_of_service(request):
    return render(request, 'terms_of_service.html')