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
from django.utils.text import slugify
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils.timezone import now

from .forms import BookingForm, EventCustomizationForm, EventTypeForm
from .models import Event, Booking, EventCustomization, AddOn, EventLocation

from .utils import get_coordinates  # Assuming get_coordinates is defined in utils.py
from django.http import JsonResponse
from fuzzywuzzy import process
from .models import ChatbotQA

import math
import json
from decimal import Decimal

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

#from .models import EventLocation, Venue, Booking, EventCustomization
from .models import EventLocation, Booking, EventCustomization  # Temporarily remove Venue

from .utils import get_coordinates
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Booking, EventCustomization

from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.utils.timezone import now
from .models import Event, Booking, EventCustomization
from .forms import BookingForm, EventCustomizationForm



from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils.timezone import now
from django.db import transaction
from django.http import JsonResponse
from decimal import Decimal
import json, math, logging

from django.contrib.auth.decorators import login_required
#from .models import Event, Booking, EventCustomization, EventLocation, AddOn
from .forms import BookingForm, EventCustomizationForm, EventTypeForm
from .utils import get_coordinates  # Assumed to exist for geocoding
import logging
import json
from decimal import Decimal
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
#from eventapp.models import Booking, EventCustomization  # Ensure correct import
from eventapp.addon_config import ADDON_CONFIG  # Ensure ADDON_CONFIG is imported correctly
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from decimal import Decimal
import json
import logging
import json
import logging
from decimal import Decimal
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages


import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction
from django.http import JsonResponse
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required
from eventapp.models import Event, Booking, EventCustomization, AddOn
from eventapp.forms import BookingForm, EventCustomizationForm, EventTypeForm
import json
from datetime import date
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import json
from .forms import EventCustomizationForm
from .addon_config import ADDON_CONFIG  # Assuming this is where your addon config is stored

from django.shortcuts import render, redirect
from django.contrib import messages
from datetime import date
import json
from .forms import EventCustomizationForm
from .addon_config import ADDON_CONFIG  # Assuming this is where your addon config is stored

import json
import logging
from decimal import Decimal
from datetime import date
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from eventapp.models import Booking, Event
from eventapp.forms import EventCustomizationForm
from eventapp.utils import calculate_total_price
from eventapp.models import EventCustomization

import json
import logging
from decimal import Decimal
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .addon_config import ADDON_CONFIG
from eventapp.models import Event

from decimal import Decimal, InvalidOperation

from decimal import Decimal, InvalidOperation

from decimal import Decimal, InvalidOperation

from decimal import Decimal, InvalidOperation
import logging
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Booking  # Import your Booking model
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from eventapp.models import Event, Booking, EventLocation
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Event, Booking, EventLocation
from .utils import get_session_booking  # Import session helper
from .utils import log_session_data



from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from .forms import BookingForm
from .models import Booking, Event
import logging



logger = logging.getLogger(__name__)

@login_required
def booking(request, slug=None):
    # Fetch the event using the slug
    event = get_object_or_404(Event, slug=slug)
    logger.debug(f"Received event slug: {slug}")

    # Save event slug in session at the start
    request.session['event_slug'] = slug
    logger.debug(f"Event slug stored in session: {request.session.get('event_slug')}")

    # Retrieve or create booking instance from session
    booking_id = request.session.get('booking_id')
    booking_instance = None
    if booking_id:
        booking_instance = Booking.objects.filter(id=booking_id, user=request.user).first()

    if request.method == "POST":
        # Handle booking form submission
        form = BookingForm(request.POST)
        if form.is_valid():
            # Save booking instance
            booking_instance = form.save(commit=False)
            booking_instance.user = request.user
            booking_instance.event = event
            booking_instance.save()

            # Save complete booking data to session for later use
            booking_data = {
                'booking_id': booking_instance.id,
                'event_slug': event.slug,
                'selected_tier': request.session.get('selected_tier', 'Minimal'),
                'selected_event_date': request.session.get('selected_event_date', ''),
                'event_location': request.session.get('event_location', {}),
                'venue_subtier': request.session.get('venue_subtier', ''),
                'cus_name': form.cleaned_data['cus_name'],
                'cus_email': form.cleaned_data['cus_email'],
                'cus_ph': form.cleaned_data['cus_ph'],
            }
            request.session['booking_data'] = booking_data
            logger.debug(f"Booking data saved to session: {request.session.get('booking_data')}")

            # Optionally log the session to verify
            logger.debug(f"Session data after booking creation: {request.session.items()}")

            messages.success(request, "Booking successful! Please proceed to the next step for customization.")
            return redirect('eventapp:event_customization', booking_id=booking_instance.id)

    else:
        form = BookingForm()

    return render(request, 'eventapp/booking.html', {
        'form': form,
        'event': event,
    })



@login_required
def select_event_type(request, slug):
    """
    Allows the user to select the event type and main tier.
    Stores the event slug, selected event type, and tier in session.
    Also ensures a Booking is created and stores its ID in session.
    """
    request.session['event_slug'] = slug
    event = get_object_or_404(Event, slug=slug)

    # Ensure a booking exists for the user and event
    booking, created = Booking.objects.get_or_create(
        user=request.user,
        event=event,
        defaults={'cus_name': request.user.get_full_name(), 'cus_email': request.user.email, "event_date": date.today()}
    )

    # Store booking ID in session
    request.session['booking_id'] = booking.id
    logger.info(f"Booking stored in session: {booking.id}")
    logger.info(f"slug = {slug}")

    if request.method == 'POST':
        form = EventTypeForm(request.POST)
        if form.is_valid():
            request.session['selected_event_type'] = form.cleaned_data['event_type']
            request.session['selected_tier'] = request.POST.get('tier', 'Minimal').capitalize()
            return redirect('eventapp:event_location')  # Proceed to location selection
    else:
        form = EventTypeForm()

    request.session.setdefault('selected_tier', 'Minimal')
    logger.debug(f"Event slug: {slug} saved in session")
    logger.debug(f"Booking created with ID: {booking.id}")
    logger.debug(f"Booking ID stored in session: {request.session.get('booking_id')}")



    return render(request, 'eventapp/select_event_type.html', {'form': form})



@login_required
def select_event_date(request):
    # Check if the event date is already set
    if 'selected_event_date' not in request.session:
        # If no event date is found, set it to today's date (default)
        request.session['selected_event_date'] = str(date.today())
        request.session.modified = True  # Ensure session updates

    # No need to render any form, just redirect to the next step
    return redirect('eventapp:customize_event')



#############################################
# Event Customization View
#############################################


logger = logging.getLogger("eventapp.customization")

@login_required
def addon_details(request, addon_name):
    """Fetches and returns addon details as JSON for the popup."""
    logger.debug(f"Fetching details for addon: {addon_name}")
    
    try:
        addon = get_object_or_404(AddOn, name=addon_name)
        options_dict = json.loads(addon.options or "{}") if isinstance(addon.options, str) else addon.options

        response_data = {
            "name": addon.name,
            "description": addon.description,
            "image_url": static(f"eventapp/images/{addon.name}.jpeg"),
            "pricing": options_dict,
            "tiers_allowed": addon.tiers_allowed,
        }

        logger.debug(f"Addon details response: {response_data}")
        return JsonResponse(response_data)
        

    except Exception as e:
        logger.error(f"Error fetching addon details: {str(e)}")
        return JsonResponse({"error": "Failed to fetch addon details"}, status=500)
    



@login_required
def customize_event(request):
    logger.debug("Accessing customize_event view")
    log_session_data(request)

    event_slug = request.session.get('event_slug')
    if not event_slug:
        messages.error(request, "Please select an event first.")
        logger.warning("No event selected in session.")
        return redirect('eventapp:select_event_type')

    selected_tier = request.session.get('selected_tier', 'Minimal')
    selected_event_date = request.session.get('selected_event_date')

    if not selected_event_date:
        messages.error(request, "Please select an event date first.")
        logger.warning("No event date selected in session.")
        return redirect('eventapp:select_event_date')

    # Ensure customization data exists in session
    request.session.setdefault('customization', {})
    customization_data = request.session['customization']
    logger.debug(f"Customization data in session: {customization_data}")

    # Prepare add-on configurations (all Boolean add-ons now)
    addon_config_json = json.dumps(ADDON_CONFIG)

    if request.method == 'POST':
        # Handle form submission
        customization_data['guest_count'] = int(request.POST.get('guest_count', 1))
        customization_data['selected_options'] = request.POST.getlist('selected_options')  # Assuming we send selected addon names
        request.session['customization'] = customization_data
        request.session.modified = True  # Ensure session changes are saved

        logger.info(f"Customization updated in session: {request.session['customization']}")
        messages.success(request, "Your event customization has been saved!")
        return redirect('eventapp:customization_summary')
    else:
        form = EventCustomizationForm(initial=customization_data, selected_tier=selected_tier)

    # Generate customization options based on selected tier (only boolean add-ons)
    customization_options = []
    for key, addon in ADDON_CONFIG.items():
        if selected_tier not in addon.get("tiers_allowed", ["Minimal", "Medium", "Premium"]):
            continue

        option_data = {
            "name": key,
            "display_name": addon.get("label", key.capitalize()),
            "image": f"/static/eventapp/images/{key}.jpeg",
            "tiers_allowed": addon.get("tiers_allowed", ["Minimal", "Medium", "Premium"]),
            "type": addon.get("type", "boolean"),
            "price": addon.get("price", 0),
            "per_guest": addon.get("per_guest", False),  # Include per_guest flag
        }

        customization_options.append(option_data)

    # Build context for rendering
    context = {
        'form': form,
        'selected_tier': selected_tier,
        'selected_event_date': selected_event_date,
        'customization_options': customization_options,
        'tier': selected_tier,
        'max_guests': {"Minimal": 50, "Medium": 100, "Premium": 200}.get(selected_tier, 50),
        'today': date.today(),
        'addon_config': addon_config_json,
    }

    logger.debug("Rendering 'customize_event.html' with provided context.")
    return render(request, 'eventapp/customize_event.html', context)


logger = logging.getLogger("eventapp.customization")

@login_required
def update_price(request):
    log_session_data(request)
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method."}, status=400)

    try:
        data = json.loads(request.body)
        logger.debug(f"🔹 Received data for price update: {json.dumps(data, indent=2)}")

        guest_count = int(data.get("guest_count", 0))
        selected_tier = request.session.get("selected_tier", "Minimal")
        event_slug = request.session.get("event_slug")  # Get event slug from session

        if not event_slug:
            logger.error("❌ No event selected in session.")
            return JsonResponse({"error": "No event selected."}, status=400)
        # Confirming slug retrieval before price calculation
        logger.debug(f"Retrieved event_slug for price update: {event_slug}")

        # Confirming slug retrieval before price calculation
        logger.debug(f"Retrieved event_slug for price update: {event_slug}")

        # Ensure guest count does not exceed tier limit
        max_guests = {"Minimal": 50, "Medium": 100, "Premium": 200}.get(selected_tier, 50)
        if guest_count > max_guests:
            logger.warning(f"⚠️ Guest count {guest_count} exceeds {selected_tier} tier limit.")
            return JsonResponse({"error": f"Guest count exceeds {selected_tier} tier limit."}, status=400)

        selected_options = []
        total_addon_price = Decimal("0.00")

        for addon_name in data.get("selected_addons", []):
            addon = ADDON_CONFIG.get(addon_name, {})
            if not addon:
                logger.warning(f"⚠️ Unrecognized add-on: {addon_name}")
                continue

            price = Decimal(addon.get("price", 0))
            if addon.get("per_guest", False):
                price *= guest_count  

            total_addon_price += price
            selected_options.append({"name": addon_name, "price": str(price)})

        # Calculate total price with event's base price
        total_price = calculate_dynamic_price(selected_tier, guest_count, total_addon_price, event_slug)
        log_session_data(request)
        # Update session safely
        customization_data = request.session.get("customization", {})
        customization_data.update({"guest_count": guest_count, "selected_options": selected_options})
        request.session["customization"] = customization_data
        request.session.modified = True

        logger.debug(f"✅ Calculated price: {total_price} for customization: {json.dumps(selected_options, indent=2)}")
        logger.debug(f"Session data at customize_event view: {request.session.items()}")

        

        return JsonResponse({
            "total_price": str(total_price),
            "selected_options": selected_options
        })

    except (ValueError, json.JSONDecodeError) as e:
        logger.error(f"❌ Invalid input data: {e}")
        return JsonResponse({"error": "Invalid input data."}, status=400)
    except Exception as e:
        logger.error(f"❌ Unexpected error updating price: {e}")
        return JsonResponse({"error": "An unexpected error occurred."}, status=500)



def calculate_dynamic_price(tier, guest_count, total_addon_price, event_slug):
    try:
        # Ensure guest_count and total_addon_price are safely converted to Decimal
        if isinstance(guest_count, (int, float)):
            guest_count = Decimal(guest_count)
        elif isinstance(guest_count, str) and guest_count.replace('.', '', 1).isdigit():
            guest_count = Decimal(guest_count)
        else:
            guest_count = Decimal("0.00")
        
        if isinstance(total_addon_price, (int, float)):
            total_addon_price = Decimal(total_addon_price)
        elif isinstance(total_addon_price, str) and total_addon_price.replace('.', '', 1).isdigit():
            total_addon_price = Decimal(total_addon_price)
        else:
            total_addon_price = Decimal("0.00")
        
        logger.debug(f"🔹 Calculating total price with base event slug: {event_slug}")
        logger.debug(f"Guest count: {guest_count}, Addon price: {total_addon_price}")
        

        # Fetch event's base estimated price
        event = get_object_or_404(Event, slug=event_slug)

        base_price = Decimal(event.estimated_price)  # Event base price
        
        logger.debug(f"Base price of event '{event_slug}': {base_price}")
        
        # Additional price per guest
        guest_price = guest_count * Decimal("500.00")
        
        logger.debug(f"Guest price for {guest_count} guests: {guest_price}")
        
        # Tier-based price adjustment
        if tier == "Premium":
            base_price += Decimal("2000.00")
        elif tier == "Medium":
            base_price += Decimal("1000.00")
        
        logger.debug(f"Adjusted base price for tier '{tier}': {base_price}")
        
        # Total price calculation
        total_price = base_price + guest_price + total_addon_price
        
        logger.debug(f"Total price calculated: {total_price}")
        
        return str(total_price)  # Return total price as a string
        

    except InvalidOperation as e:
        logger.error(f"❌ Invalid operation in price calculation: {e}")
        return str(Decimal("0.00"))  # Return zero if an error occurs during the calculation

    except Event.DoesNotExist:
        logger.warning(f"⚠️ Event with slug {event_slug} not found. Using default price.")
        return str(Decimal("0.00"))

    except Exception as e:
        logger.error(f"❌ Unexpected error in price calculation: {e}")
        return str(Decimal("0.00"))  # Return zero if any other error occurs


#############################################
# Customization Summary
#############################################


def customization_summary(request, booking_id):
    log_session_data(request)
    booking = get_object_or_404(Booking, id=booking_id)
    
    # Retrieve all necessary data from the session
    selected_venue = request.session.get('selected_venue', '')
    event_location_name = request.session.get('event_location', '')
    customization = request.session.get('customization', {})
    event_slug = request.session.get('event_slug', '')  # Ensure this is a string
    selected_tier = request.session.get('selected_tier', '')  # Ensure this is retrieved as well
    
    logger.debug(f"Retrieved customization from session: {customization}")
    logger.debug(f"Selected venue from session: {selected_venue}")
    logger.debug(f"Event slug from session: {event_slug}")
    logger.debug(f"Selected tier from session: {selected_tier}")
    logger.debug(f"Session data at customize_event view: {request.session.items()}")

    
    # Get the event_slug from session (no need to fetch from booking)
    if not event_slug:
        event_slug = booking.event.slug  # Fallback to booking event if session value is missing
    
    # Calculate the total price
    total_price = calculate_dynamic_price(
        selected_tier,  # Pass the selected tier
        customization.get('guest_count', 0),  # Get guest count from customization
        sum([Decimal(option['price']) for option in customization.get('selected_options', [])]),  # Sum addon prices
        event_slug  # Pass the event slug here
    )
    
    # Prepare context
    context = {
        'customization': customization,
        'selected_venue': selected_venue,
        'event_location': event_location_name,
        'venue_tier': selected_tier,
        'guest_count': customization.get('guest_count', 0),
        'total_price': total_price,
        'selected_addons': customization.get('selected_options', []),
        'booking': booking,
    }

    # Log the customization data for debugging
    logger.debug(f"Customization summary data: {context}")

    return render(request, 'eventapp/customization_summary.html', context)



#############################################
# Location Picker View
#############################################

@login_required
def event_location(request):
    """
    Handles event location selection using session-stored booking information.
    """
    session_data = get_session_booking(request)  # Fetch session data

    if not session_data['event_slug']:
        messages.error(request, "Please select an event first.")
        return redirect('eventapp:select_event_type')

    event = get_object_or_404(Event, slug=session_data['event_slug'])

    if not session_data['booking_id']:
        messages.error(request, "No booking found. Please start over.")
        return redirect('eventapp:select_event_type', slug=session_data['event_slug'])

    # Retrieve existing booking (ensures it exists instead of creating a new one)
    booking = get_object_or_404(Booking, id=session_data['booking_id'], user=request.user)

    # Retrieve or create event location instance
    location_instance, _ = EventLocation.objects.get_or_create(booking=booking)

    if request.method == 'POST':
        full_address = request.POST.get('full_address')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        pincode = request.POST.get('pincode')
        place_id = request.POST.get('place_id')

        if full_address and latitude and longitude:
            location_instance.full_address = full_address
            location_instance.latitude = float(latitude)
            location_instance.longitude = float(longitude)
            location_instance.pincode = pincode
            location_instance.place_id = place_id
            location_instance.save()

            # Store location in session
            request.session['event_location'] = {
                "full_address": full_address,
                "latitude": latitude,
                "longitude": longitude,
                "pincode": pincode,
                "place_id": place_id,
            }

            messages.success(request, "Location saved successfully.")
            return redirect('eventapp:select_venue_tier')

    return render(request, 'eventapp/event_location.html', {'event': event, 'booking': booking, 'location': location_instance})


#############################################
# Venue Tier Selection View
#############################################
@login_required
def select_venue_tier(request):
    selected_tier = request.session.get('selected_tier', 'Minimal')
    event_location_name = request.session.get('event_location', None)
    allowed_subtiers = get_allowed_subtiers(selected_tier)

    venue_subtier_pricing = {"Minimal": Decimal('0'), "Medium": Decimal('300'), "Luxury": Decimal('600')}
    enhanced_subtiers = [(t, f"{t} (+${venue_subtier_pricing.get(t, Decimal('0'))})") for t in allowed_subtiers]

    if request.method == 'POST':
        chosen_subtier = request.POST.get('venue_subtier')
        custom_desc = request.POST.get('custom_venue_description', '')

        if not chosen_subtier:
            messages.error(request, "Please select a venue sub-tier.")
            return redirect('eventapp:select_venue_tier')

        if not is_valid_subtier(chosen_subtier, allowed_subtiers):
            messages.error(request, "Invalid venue selection for your tier.")
            return redirect('eventapp:select_venue_tier')

        # 🚀 Save venue data in session
        request.session['selected_venue'] = "Custom" if chosen_subtier == "Custom" else chosen_subtier
        request.session['venue_subtier'] = chosen_subtier
        request.session['custom_venue_description'] = custom_desc if chosen_subtier == "Custom" else ""

        messages.success(request, "Venue selection saved!")
        return redirect('eventapp:customize_event')

    return render(request, 'eventapp/select_venue_tier.html', {
        'selected_tier': selected_tier,
        'allowed_subtier_names': allowed_subtiers,
        'enhanced_subtiers': enhanced_subtiers,
        'event_location': event_location_name,
    })


#############################################
# Helper Functions
#############################################
def get_allowed_subtiers(selected_tier):
    """Determine allowed venue sub-tiers based on the main event tier."""
    return {
        "Minimal": ["Minimal"],
        "Medium": ["Minimal", "Medium"],
        "Premium": ["Minimal", "Medium", "Luxury"]
    }.get(selected_tier, ["Minimal"])


def is_valid_subtier(subtier, allowed_subtiers):
    """Check if the selected subtier is valid for the event tier."""
    return subtier in allowed_subtiers or subtier == "Custom"



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

def index(request):
    # Get all available future events
    events = Event.objects.filter(available_until__gte=now().date(), is_available=True)


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
    events = Event.objects.filter(available_until__gte=now().date(), is_available=True).order_by('available_until')  
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

def event_detail(request, slug):
    event = get_object_or_404(Event, slug=slug)
    related_events = Event.objects.filter(event_type=event.event_type).exclude(id=event.id).order_by('?')[:3]
    
    # Redirect users to the booking page
    if request.method == "POST":
        return redirect('eventapp:booking', slug=slug)

    return render(request, 'eventapp/event_details.html', {'event': event, 'related_events': related_events})


def privacy_policy(request):
    return render(request, 'privacy_policy.html')
def terms_of_service(request):
    return render(request, 'terms_of_service.html')

# eventapp/views.py/chatbot-view

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
