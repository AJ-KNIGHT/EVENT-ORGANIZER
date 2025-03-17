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
import json
from .models import Event, Booking, EventCustomization
from .forms import BookingForm, EventCustomizationForm, EventTypeForm


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from .models import Event, Booking, EventCustomization
from .forms import BookingForm, EventCustomizationForm, EventTypeForm
from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .forms import EventCustomizationForm, EventTypeForm
from .models import Event, Booking, EventCustomization
from .addon_config import ADDON_CONFIG  # Make sure this file exists as per our plan

import json
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import EventCustomizationForm
from .models import Event, Booking, EventCustomization
from .addon_config import ADDON_CONFIG  # This file should define your addon configuration.

from django.http import JsonResponse
from decimal import Decimal
from .models import AddOn
import json
from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

from .forms import EventCustomizationForm, EventTypeForm
from .models import Event, Booking, EventCustomization

from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import EventTypeForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import json
from .models import Booking, EventCustomization, AddOn
from .forms import EventCustomizationForm
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Booking, EventCustomization
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required
from .forms import BookingForm, EventCustomizationForm, EventTypeForm
from .models import Event, Booking, EventCustomization
import json
import math
import requests
from decimal import Decimal

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils.timezone import now

from .forms import BookingForm, EventCustomizationForm, EventTypeForm
from .models import Event, Booking, EventCustomization, AddOn, EventLocation
from .addon_config import ADDON_CONFIG
from .utils import get_coordinates  # Assuming get_coordinates is defined in utils.py



def clear_booking_session(request):
    """Clears booking-related session data after booking completion."""
    for key in ['event_slug', 'selected_event_type', 'base_price', 'booking_id', 'selected_tier', 'event_location', 'user_lat', 'user_lon']:
        request.session.pop(key, None)


def booking(request, slug=None):
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
            
            # Save session data for later use during payment
            request.session['booking_data'] = {
                'event_id': event.id,
                'cus_name': request.user.get_full_name(),
                'cus_email': request.user.email,
                'venue': booking.venue,
                'total_amount': booking.total_amount,
            }

            # Handle customization and update total amount
            customization, _ = EventCustomization.objects.get_or_create(booking=booking)
            customization_form = EventCustomizationForm(request.POST, instance=customization)
            if customization_form.is_valid():
                customization_form.save()

            booking.total_amount = customization.calculate_price()
            booking.save(update_fields=['total_amount'])
            messages.success(request, "Booking successful! Your customization has been applied.")
            return redirect('paymentapp:payment_page')
    else:
        initial_data = {'cus_name': request.user.get_full_name(), 'cus_email': request.user.email}
        booking_form = BookingForm(initial=initial_data)
        customization_form = EventCustomizationForm()

    return render(request, 'eventapp/booking.html', {
        'booking_form': booking_form,
        'customization_form': customization_form,
        'event': event,
    })


@login_required
def select_event_type(request):
    """
    Allows the user to select the event type and tier.
    Stores the event slug, selected event type, and tier in session.
    """
    event_slug = request.GET.get('event')
    if event_slug:
        request.session['event_slug'] = event_slug

    if request.method == 'POST':
        form = EventTypeForm(request.POST)
        if form.is_valid():
            request.session['selected_event_type'] = form.cleaned_data['event_type']
            # Get tier from POST (if provided) and store it in session.
            request.session['selected_tier'] = request.POST.get('tier', 'Minimal').capitalize()
            return redirect('eventapp:event_location')  # Redirect to Event Location page
    else:
        form = EventTypeForm()

    return render(request, 'eventapp/select_event_type.html', {'form': form})


@login_required
def customize_event(request):
    """
    Handles event customization. Ensures a booking exists, then retrieves or creates the EventCustomization instance.
    Uses the selected tier (from session or GET parameter) to dynamically build allowed addon options and initialize the form.
    Also passes the chosen venue, location, and venue tier to the template.
    """
    event_slug = request.session.get('event_slug')
    if not event_slug:
        messages.error(request, "Please select an event first.")
        return redirect('eventapp:select_event_type')

    event = get_object_or_404(Event, slug=event_slug)
    selected_tier = request.session.get('selected_tier', 'Minimal')

    # Create (or retrieve) the booking.
    booking, created = Booking.objects.get_or_create(user=request.user, event=event,defaults={
        'event_date': event.event_date,   # Use the event's date as default
        'cus_name': request.user.get_full_name(),
        'cus_email': request.user.email,
    })
    
    # Ensure the booking is saved before proceeding to the EventCustomization creation
    booking.save()

    request.session['booking_id'] = booking.id

    # Store the booking data in the session (convert Decimal to float for total_amount)
    request.session['booking_data'] = {
        'event_id': event.id,
        'cus_name': request.user.get_full_name(),
        'cus_email': request.user.email,
        'venue': booking.venue,
        'total_amount': float(booking.total_amount),  # Convert Decimal to float
    }

    # Retrieve (or create) the customization instance.
    customization, _ = EventCustomization.objects.get_or_create(booking=booking)

    # Optionally override tier from GET parameters.
    if request.GET.get('tier'):
        selected_tier = request.GET.get('tier').capitalize()
    if customization.tier != selected_tier:
        customization.tier = selected_tier
        customization.save(update_fields=['tier'])

    if request.method == 'POST':
        form = EventCustomizationForm(request.POST, instance=customization, selected_tier=selected_tier)
        if form.is_valid():
            customization = form.save()
            booking.total_amount = customization.calculate_price()
            booking.save(update_fields=['total_amount'])
            messages.success(request, "Your event customization has been saved!")
            return redirect('eventapp:customization_summary', booking_id=booking.id)
    else:
        form = EventCustomizationForm(instance=customization, selected_tier=selected_tier)

    # Build allowed addon options from ADDON_CONFIG based on the selected tier.
    customization_options = []
    for key, addon in ADDON_CONFIG.items():
        tiers_allowed = addon.get("tiers_allowed", ["Minimal", "Medium", "Premium"])
        if selected_tier in tiers_allowed:
            customization_options.append({
                "name": key,
                "display_name": addon.get("label", key.capitalize()),
                "image": f"/static/eventapp/images/{key}.png",
                "tiers_allowed": tiers_allowed,
            })

    # Retrieve additional details from session:
    selected_venue = request.session.get('selected_venue', '')
    location_name = request.session.get('event_location', '')
    venue_tier = request.session.get('selected_tier', '')
    print(f"Booking Data in Session: {request.session.get('booking_data')}")


    context = {
        'form': form,
        'booking': booking,
        'selected_tier': selected_tier,
        'selected_options_json': json.dumps(customization.selected_options or {}),
        'customization_options': customization_options,
        'addon_config': ADDON_CONFIG,
        'tier': selected_tier,  # for template hidden input
        'selected_venue': selected_venue,
        'location_name': location_name,
        'venue_tier': venue_tier,
    }
    return render(request, 'eventapp/customize_event.html', context)





@login_required
def customization_summary(request, booking_id):
    """Displays the customization summary before proceeding to payment."""
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    customization = get_object_or_404(EventCustomization, booking=booking)

    # Retrieve selected venue and location from session.
    selected_venue = request.session.get('selected_venue', '')
    event_location_name = request.session.get('event_location', '')
    print(f"Booking Data in Session: {request.session.get('booking_data')}")


    # Prepare the context for the template
    context = {
        'booking': booking,
        'customization': customization,
        'selected_venue': selected_venue,
        'event_location': event_location_name,
        'venue_tier': request.session.get('selected_tier', ''),
    }

    return render(request, 'eventapp/customization_summary.html', context)




def update_price(request):
    """
    AJAX view to update the total price.
    Expects 'tier', 'guest_count', and 'selected_options' in POST data.
    Returns a JSON response with the calculated total price.
    The calculation multiplies (base price + addon cost) by guest count.
    (The final price is computed by the model upon form submission.)
    """
    if request.method == "POST":
        tier = request.POST.get('tier', 'Minimal').capitalize()
        try:
            guest_count = int(request.POST.get('guest_count', 0))
        except ValueError:
            return JsonResponse({"error": "Invalid guest count."}, status=400)

        # Enforce tier-specific guest limits.
        tier_guest_limits = {"Minimal": 50, "Medium": 100, "Premium": 200}
        if guest_count > tier_guest_limits.get(tier, 50):
            return JsonResponse({"error": f"Guest count exceeds {tier} tier limit."}, status=400)

        # Base price by tier.
        tier_pricing = {"Minimal": Decimal('0'), "Medium": Decimal('500'), "Premium": Decimal('1000')}
        base_price = tier_pricing.get(tier, Decimal('0'))

        # Simplified addon cost mapping for AJAX price estimation.
        addon_costs = {
            "catering": Decimal('300'),
            "entertainment": Decimal('200'),
            "decorations": Decimal('100'),
            "event_manager": Decimal('100'),
            "medical_support": Decimal('100'),
            "cleanup_service": Decimal('100'),
            "lighting_effects": Decimal('100'),
            "audio_visual": Decimal('100'),
            "photography": Decimal('100'),
        }


        selected_options = request.POST.getlist('selected_options[]', [])


        extra_cost = sum(addon_costs.get(opt, Decimal('0')) for opt in selected_options)

        total_price = (base_price + extra_cost) * guest_count
        return JsonResponse({"total_price": str(total_price)})

    return JsonResponse({"error": "Invalid request method."}, status=400)


def event_detail(request, slug):
    event = get_object_or_404(Event, slug=slug)
    related_events = Event.objects.filter(event_type=event.event_type).exclude(id=event.id).order_by('?')[:3]
    return render(request, 'eventapp/event_details.html', {'event': event, 'related_events': related_events})


import math
import json
from decimal import Decimal

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import EventLocation, Venue, Booking, EventCustomization
from .utils import get_coordinates

#############################################
# Helper Functions for Location/Map
#############################################

def haversine(lat1, lon1, lat2, lon2):
    """Calculate the great-circle distance between two points."""
    R = 6371  # Earth radius in km
    dlat = math.radians(float(lat2) - float(lat1))
    dlon = math.radians(float(lon2) - float(lon1))
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(float(lat1))) * math.cos(math.radians(float(lat2))) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def find_nearby_venues(user_lat, user_lon, venues):
    """Find venues within 10 km of the given user coordinates (if needed)."""
    user_lat, user_lon = float(user_lat), float(user_lon)
    nearby = []
    for venue in venues:
        venue_lat, venue_lon = float(venue["lat"]), float(venue["lon"])
        distance = haversine(user_lat, user_lon, venue_lat, venue_lon)
        if distance <= 10:
            nearby.append({**venue, "distance": round(distance, 2)})
    return nearby

#############################################
# Location Picker View
#############################################
@login_required
def event_location(request):
    """
    View for picking an event location using a map (Leaflet) and/or search.
    Saves or updates the chosen location (name and coordinates) for the current booking,
    and stores the location name in session.
    Carries over the main event tier to the next step.
    """
    # Check if there's a 'tier' parameter in the GET request; update session tier if present.
    if 'tier' in request.GET:
        request.session['selected_tier'] = request.GET['tier'].capitalize()

    nearby_venues = []  # (For legacy purposes; may be unused.)

    if request.method == 'POST':
        location = request.POST.get('location')
        lat = request.POST.get('latitude')
        lon = request.POST.get('longitude')

        # If lat/lon is missing, try geocoding the location name.
        if not lat or not lon:
            lat, lon = get_coordinates(location)

        if lat is not None and lon is not None:
            # Check if there's an existing booking.
            booking_id = request.session.get('booking_id')
            if booking_id:
                booking = get_object_or_404(Booking, id=booking_id)
                # Update or create the EventLocation record linked to this booking.
                event_loc, created = EventLocation.objects.update_or_create(
                    booking=booking,
                    defaults={
                        'name': location,
                        'latitude': float(lat),
                        'longitude': float(lon)
                    }
                )
            else:
                # If no booking exists yet, create an unlinked EventLocation record.
                event_loc = EventLocation.objects.create(
                    name=location,
                    latitude=float(lat),
                    longitude=float(lon)
                )
            # Store location data in the session.
            request.session['event_location'] = location
            request.session['user_lat'] = float(lat)
            request.session['user_lon'] = float(lon)

            messages.success(request, "Location saved successfully!")
            # Redirect to the venue tier selection page.
            return redirect('eventapp:select_venue_tier')
        else:
            return JsonResponse({'error': 'Could not find location, try again'}, status=400)

    # On GET, render the location picking template.
    context = {
        'nearby_venues': nearby_venues,
    }
    return render(request, 'eventapp/event_location.html', context)



#############################################
# Venue Tier Selection View
#############################################
@login_required
def select_venue_tier(request):
    """
    Separate page for selecting the internal venue tier (Minimal, Medium, Luxury)
    based on the main event tier and optionally the picked location.
    """
    # Retrieve main event tier from session
    selected_tier = request.session.get('selected_tier', 'Minimal')
    # Retrieve the picked location name from session (if available)
    event_location_name = request.session.get('event_location', None)

    # Determine allowed venue sub-tiers based on main event tier.
    if selected_tier == "Minimal":
        allowed_subtiers = ["Minimal"]
    elif selected_tier == "Medium":
        allowed_subtiers = ["Minimal", "Medium"]
    else:  # Premium (or higher)
        allowed_subtiers = ["Minimal", "Medium", "Luxury"]

    if request.method == 'POST':
        chosen_subtier = request.POST.get('venue_subtier')
        custom_desc = request.POST.get('custom_venue_description', '')

        booking_id = request.session.get('booking_id')
        booking = get_object_or_404(Booking, id=booking_id)
        customization, _ = EventCustomization.objects.get_or_create(booking=booking)

        # Validate the chosen sub-tier
        if chosen_subtier not in allowed_subtiers and chosen_subtier != 'Custom':
            messages.error(request, "Invalid venue selection for your tier.")
            return redirect('eventapp:select_venue_tier')

        # Save sub-tier (or custom) to the EventCustomization model and update session
        if chosen_subtier == 'Custom':
            customization.venue_subtier = 'Custom'
            customization.custom_venue_description = custom_desc
            request.session['selected_venue'] = "Custom"
        else:
            customization.venue_subtier = chosen_subtier
            customization.custom_venue_description = ''
            request.session['selected_venue'] = chosen_subtier

        customization.save()
        messages.success(request, "Venue selection saved!")
        return redirect('eventapp:customize_event')

    context = {
        'selected_tier': selected_tier,
        'allowed_subtiers': allowed_subtiers,
        'event_location': event_location_name,
    }
    return render(request, 'eventapp/select_venue_tier.html', context)




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
