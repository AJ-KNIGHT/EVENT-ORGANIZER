from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Event, Booking , Contact
from datetime import date
from .forms import BookingForm ,ChangeRequestForm 
from django.utils.timezone import now
from django.core.mail import send_mail
from django.conf import settings
from django.core.paginator import Paginator
from django.utils import timezone
from django.utils.timezone import make_aware
from datetime import datetime
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

@login_required
def booking(request, slug=None):
    event = get_object_or_404(Event, slug=slug)

    # Check if the event is bookable
    if event.event_date < date.today() or not event.is_available:
        messages.error(request, "Sorry, this event is not available for booking yet.")
        return redirect('events')

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            print('Form is valid')

            # Create booking instance but don't save it yet
            booking = form.save(commit=False)

            # Manually assign the user (since it's excluded from the form)
            booking.user = request.user

            # Set the event data (event_name and event_date)
            booking.event_name = event
            booking.event_date = event.event_date

            # Set the total amount (price of the event)
            booking.total_amount = event.price

            # Save the booking to the database
            booking.save()
            print(f"Booking created: {booking}")
            print(f"Booking user: {booking.user}")
            print(f"Event: {booking.event_name}")

            # Send email notifications (user and admin)

            # Email to user (booking confirmation)
            send_mail(
                f"Booking Confirmation for {event.name}",
                '',
                settings.EMAIL_HOST_USER,
                [booking.cus_email],
                fail_silently=False,
                html_message=f'''
                    <html>
                        <body>
                            <h3 style="color: green;">Booking Confirmation</h3>
                            <p>Hello <strong>{booking.cus_name}</strong>,</p>
                            <p>Thank you for booking the event <strong>{event.name}</strong>.</p>
                            <p>Your booking has been confirmed for the following event:</p>
                            <ul>
                                <li><strong>Event Name:</strong> {event.name}</li>
                                <li><strong>Event Date:</strong> {event.event_date}</li>
                                <li><strong>Venue:</strong> {booking.venue}</li>
                                <li><strong>Total Amount:</strong> ${booking.total_amount}</li>
                            </ul>
                            <p>We look forward to seeing you at the event!</p>
                            <p><em>If you need any assistance or want to make changes to your booking, feel free to contact us.</em></p>
                            <p>Best regards,<br>The EventPro Team</p>
                        </body>
                    </html>
                '''
            )

            # Email to admin (new booking notification)
            send_mail(
                f"New Booking for {event.name}",
                '',
                settings.EMAIL_HOST_USER,
                [settings.ADMIN_EMAIL],
                fail_silently=False,
                html_message=f'''
                    <html>
                        <body>
                            <h3 style="color: blue;">New Booking Notification</h3>
                            <p>A new booking has been made for the event <strong>{event.name}</strong> by <strong>{booking.cus_name}</strong>.</p>
                            <p><strong>Event Date:</strong> {event.event_date}</p>
                            <p><strong>Venue:</strong> {booking.venue}</p>
                            <p><strong>Total Amount:</strong> ${booking.total_amount}</p>
                            <p>To view or manage this booking, visit the admin panel.</p>
                            <p>Best regards,<br>The EventPro Team</p>
                        </body>
                    </html>
                '''
            )

            messages.success(request, "Your event has been booked successfully!")
            return redirect('userapp:booking_dashboard')  # Redirect to booking dashboard
        else:
            print(f"Form Errors: {form.errors}")
            messages.error(request, "There was an error with your booking. Please check the form and try again.")
    else:
        # Pre-populate the form with the event data
        form = BookingForm(event_instance=event)

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








def privacy_policy(request):
    return render(request, 'privacy_policy.html')
def terms_of_service(request):
    return render(request, 'terms_of_service.html')