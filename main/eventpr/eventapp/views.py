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
from .forms import EventCustomizationForm , EventTypeForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.templatetags.static import static
from django.conf import settings
from datetime import date

from eventapp.models import Event, Booking
from eventapp.forms import BookingForm
from paymentapp.models import Payment  # Import Payment model
from paymentapp.views import confirm_payment  # Import confirm_payment function
from userapp.utils import send_html_email  # Import email function



from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from decimal import Decimal
from .models import Event, Booking, EventCustomization
from .forms import BookingForm, EventCustomizationForm, EventTypeForm
from django.templatetags.static import static

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required

from .models import Event, Booking, EventCustomization
from .forms import BookingForm, EventCustomizationForm, EventTypeForm


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from .models import Event, Booking, EventCustomization
from .forms import BookingForm, EventCustomizationForm, EventTypeForm

def clear_booking_session(request):
    """Clears booking-related session data after booking completion."""
    for key in ['event_slug', 'selected_event_type', 'base_price']:
        if key in request.session:
            del request.session[key]

@login_required
def booking(request, slug=None):
    """Handles event booking and customization."""
    event = get_object_or_404(Event, slug=slug)

    if event.event_date < now().date() or not event.is_available:
        messages.error(request, "This event is no longer available for booking.")
        return redirect('event_detail', slug=slug)

    if request.method == "POST":
        booking_form = BookingForm(request.POST)
        customization_form = EventCustomizationForm(request.POST)

        if booking_form.is_valid() and customization_form.is_valid():
            booking = booking_form.save(commit=False)
            booking.user = request.user
            booking.event = event
            booking.event_date = event.event_date
            booking.save()

            customization, _ = EventCustomization.objects.get_or_create(booking=booking)
            customization_form = EventCustomizationForm(request.POST, instance=customization)
            if customization_form.is_valid():
                customization_form.save()

            booking.total_amount = customization.calculate_price()
            booking.save(update_fields=['total_amount'])

            messages.success(request, "Booking successful! Your customization has been applied.")
            clear_booking_session(request)  # Clear session data after booking
            return redirect('booking_dashboard')
    else:
        # Prefill form with user details if available
        initial_data = {
            'cus_name': request.user.get_full_name(),
            'cus_email': request.user.email,
        }
        booking_form = BookingForm(initial=initial_data)
        customization_form = EventCustomizationForm()

    return render(request, 'eventapp/booking.html', {
        'booking_form': booking_form,
        'customization_form': customization_form,
        'event': event,
    })

@login_required
def select_event_type(request):
    """Allows users to select an event type before customization."""
    event_slug = request.GET.get('event')
    if event_slug:
        request.session['event_slug'] = event_slug

    if request.method == 'POST':
        form = EventTypeForm(request.POST)
        if form.is_valid():
            request.session['selected_event_type'] = form.cleaned_data['event_type']
            return redirect('eventapp:customize_event')
    else:
        form = EventTypeForm()

    return render(request, 'eventapp/select_event_type.html', {'form': form})

@login_required
def customize_event(request):
    """Allows users to customize their event after selecting the type."""
    
    selected_event_type = request.session.get('selected_event_type')
    event_slug = request.session.get('event_slug')

    if not selected_event_type or not event_slug:
        messages.error(request, "Please select an event type first.")
        return redirect('eventapp:select_event_type')

    event = get_object_or_404(Event, slug=event_slug)

    booking = Booking.objects.filter(user=request.user, event=event, status='Pending').order_by('-booking_date').first()
    if not booking:
        messages.error(request, "You have no active bookings to customize.")
        return redirect('eventapp:select_event_type')

    customization, _ = EventCustomization.objects.get_or_create(booking=booking)
    

    if request.method == 'POST':
        form = EventCustomizationForm(request.POST, instance=customization)
        if form.is_valid():
            customization = form.save()
            booking.total_amount = customization.calculate_price()
            booking.save(update_fields=['total_amount'])
            messages.success(request, "Your event customization has been saved!")
            return redirect('eventapp:customization_summary', booking_id=booking.id)

    else:
        form = EventCustomizationForm(instance=customization)

    return render(request, 'eventapp/customize_event.html', {'form': form, 'event': event})


@login_required
def customization_summary(request, booking_id):
    """Displays the customization summary before payment."""
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    customization = get_object_or_404(EventCustomization, booking=booking)
    return render(request, 'eventapp/customization_summary.html', {
        'booking': booking,
        'customization': customization,
    })

def event_detail(request, slug):
    event = get_object_or_404(Event, slug=slug)
    related_events = Event.objects.filter(event_type=event.event_type).exclude(id=event.id).order_by('?')[:3]
    return render(request, 'eventapp/event_details.html', {'event': event, 'related_events': related_events})

import math
import requests
from django.shortcuts import render
from django.http import JsonResponse

# Function to get latitude and longitude from location (OpenStreetMap API)
def get_coordinates(location):
    url = f"https://nominatim.openstreetmap.org/search?q={location}&format=json"
    response = requests.get(url)
    data = response.json()
    
    if data:
        latitude = data[0]["lat"]
        longitude = data[0]["lon"]
        return latitude, longitude
    return None, None

# Haversine formula to calculate the distance between two coordinates
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Radius of the Earth in km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c  # Distance in km

# Function to find nearby venues based on the user's location
def find_nearby_venues(user_lat, user_lon, venues, radius=5):
    nearby_venues = []
    for venue in venues:
        venue_lat, venue_lon = venue['lat'], venue['lon']
        distance = haversine(user_lat, user_lon, venue_lat, venue_lon)
        if distance <= radius:
            nearby_venues.append(venue)
    return nearby_venues

# View to handle location input and display nearby venues
def event_location(request):
    nearby_venues = []
    
    if request.method == 'POST':
        location = request.POST.get('location')
        lat, lon = get_coordinates(location)
        
        if lat and lon:
            # Example venues (replace this with your actual venue data)
            venues = [
                {'name': 'Venue 1', 'lat': 28.6100, 'lon': 77.2100},
                {'name': 'Venue 2', 'lat': 28.6000, 'lon': 77.2000},
                {'name': 'Venue 3', 'lat': 28.5500, 'lon': 77.1500},
                {'name': 'Venue 4', 'lat': 28.6200, 'lon': 77.2200}
            ]
            nearby_venues = find_nearby_venues(lat, lon, venues)
            return render(request, 'event_location.html', {'latitude': lat, 'longitude': lon, 'nearby_venues': nearby_venues})
        else:
            return JsonResponse({'error': 'Location not found'}, status=400)
    
    return render(request, 'event_location.html', {'nearby_venues': nearby_venues})


def index(request):
    # Get all available future events
    events = Event.objects.filter(event_date__gte=now().date(), is_available=True)

    # Fetch random events
    random_events = events.order_by('?')[:3] if events.count() >= 3 else events

    # Preloaded assets for better UX
    preloaded_assets = {'video': static('images/pexel-party.mp4')}

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
    return render(request, 'eventapp/events.html', {'page_obj': page_obj})

# Contact view
def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        Contact.objects.create(name=name, email=email, message=message)
        request.toast_type = 'success'  # 'error', 'warning', 'info', etc.
        request.toast_message = 'Thank you for reaching out! We will get back to you soon.'
        messages.success(request, 'Thank you for reaching out! We will get back to you soon.')
        return redirect('contact')

    # Now pass the messages_list to your template context
    preloaded_assets ={
        'contact_image': static('images/pexel-contact.jpg'),
    }
    return render(request, 'contact.html', {'preloaded_assets': preloaded_assets,})



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

# eventapp/views.py/chatbot-view


from django.http import JsonResponse
from fuzzywuzzy import process
from .models import ChatbotQA

def chatbot_response(request):
    try:
        user_input = request.GET.get('input', '').strip().lower()
        if not user_input:
            return JsonResponse({'response': "Please type something!"})

        # Get all questions and keywords from the database
        qa_pairs = ChatbotQA.objects.values_list('question', 'keywords')
        print("QA Pairs from database:", qa_pairs)  # Debugging log

        # If no data exists, return a default response
        if not qa_pairs:
            return JsonResponse({'response': "I'm still learning. Please check back later!"})

        # Combine questions and keywords for matching
        all_options = []
        for question, keywords in qa_pairs:
            all_options.append(question)
            if keywords:
                all_options.extend(keywords.split(','))
        print("All options for matching:", all_options)  # Debugging log

        # Find the best match using fuzzy matching
        best_match, score = process.extractOne(user_input, all_options)
        print("Best match and score:", best_match, score)  # Debugging log

        if score >= 70:  # Adjust threshold as needed
            # Find the question corresponding to the best match
            for question, keywords in qa_pairs:
                if best_match == question or best_match in (keywords.split(',') if keywords else []):
                    answer = ChatbotQA.objects.get(question=question).answer
                    return JsonResponse({'response': answer})
        else:
            return JsonResponse({'response': "I'm sorry, I didn't understand that. Can you please rephrase your question?"})
        

    except Exception as e:
        # Log the error for debugging
        print(f"Error in chatbot_response: {e}")
        return JsonResponse({'response': "An error occurred. Please try again later." }, status=500)
