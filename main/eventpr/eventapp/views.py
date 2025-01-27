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
from eventpr.utils import send_html_email
from django.db.models import Count
from django.utils.timezone import now
from django.shortcuts import render
from .models import Event
from django.templatetags.static import static


def index(request):
    # Get all events that are available and not in the past
    events = Event.objects.filter(event_date__gte=now().date(), is_available=True)

    # If fewer than 3 events, show all of them, else show 3 random events
    if events.count() < 3:
        random_events = events
    else:
        random_events = events.order_by('?')[:3]  # Randomly order and limit to 3 events

    # Define preloaded assets for the index page
    preloaded_assets = {
        'video': static('images/pexel-party.mp4'),
        
    }

    # Pass both the events and preloaded assets to the template
    return render(request, 'index.html', {'events': random_events, 'preloaded_assets': preloaded_assets})





# About view
def about(request):
    preloaded_assets ={
        'about_image': static('images/pexel-about.jpg'),
    }
    return render(request, 'about.html', {'preloaded_assets': preloaded_assets})

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





@login_required
def booking(request, slug=None):
    event = get_object_or_404(Event, slug=slug)

    if event.event_date < date.today() or not event.is_available:
        messages.error(request, "Sorry, this event is not available for booking yet.")
        return redirect('events')

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.event_name = event
            booking.event_date = event.event_date
            booking.total_amount = event.price
            booking.save()

            # Email to user
            user_email_context = {
                'cus_name': booking.cus_name,
                'event_name': event.name,
                'event_date': event.event_date,
                'venue': booking.venue,
                'total_amount': booking.total_amount,
            }
            send_html_email(
                subject=f"Booking Confirmation for {event.name}",
                template_name='email/booking_confirmation_email.html',
                context=user_email_context,
                recipient_list=[booking.cus_email],
            )

            # Email to admin
            admin_email_context = {
                'event_name': event.name,
                'event_date': event.event_date,
                'cus_name': booking.cus_name,
                'venue': booking.venue,
                'total_amount': booking.total_amount,
            }
            send_html_email(
                subject=f"New Booking for {event.name}",
                template_name='email/new_booking_notification.html',
                context=admin_email_context,
                recipient_list=[settings.ADMIN_EMAIL],
            )

            messages.success(request, "Your event has been booked successfully!")
            return redirect('userapp:booking_dashboard')
        else:
            messages.error(request, "There was an error with your booking. Please check the form and try again.")
    else:
        form = BookingForm(event_instance=event)
    
    preloaded_assets = {
        'hero_image': static('images/hero-bg.jpg'),
    }
    
    context = {
        'form': form,
        'event': event,
        'preloaded_assets': preloaded_assets,
    }

    return render(request, 'booking.html', context)



# Contact view
def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        Contact.objects.create(name=name, email=email, message=message)
        messages.success(request, 'Thank you for reaching out! We will get back to you soon.')
        return redirect('contact')
    preloaded_assets ={
        'contact_image': static('images/pexel-contact.jpg'),
    }
    return render(request, 'contact.html', {'preloaded_assets': preloaded_assets})


from datetime import datetime

def base(request):
    context = {
        'current_year': datetime.now().year,
    }
    return render(request, 'base.html', context)



def privacy_policy(request):
    return render(request, 'privacy_policy.html')
def terms_of_service(request):
    return render(request, 'terms_of_service.html')






