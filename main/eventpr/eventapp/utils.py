import requests

def get_coordinates(location):
    url = f"https://nominatim.openstreetmap.org/search?q={location}&format=json"
    headers = {"User-Agent": "EventOrganizerApp/1.0 (eventpro49@gmail.com)"}  # Nominatim requires a User-Agent

    try:
        response = requests.get(url, headers=headers)

        # ✅ Check if response is successful
        if response.status_code != 200:
            print(f"Error: Nominatim returned status {response.status_code}")
            return None, None

        data = response.json()

        # ✅ Check if response contains location data
        if not data:
            print("Nominatim returned an empty response.")
            return None, None

        return float(data[0]["lat"]), float(data[0]["lon"])

    except requests.exceptions.RequestException as e:
        print(f"Request Error: {e}")
        return None, None  # Handle failure gracefully
    except ValueError as e:
        print(f"Error parsing JSON: {e}")
        return None, None

import logging

logger = logging.getLogger(__name__)

def get_session_booking(request):
    """
    Retrieve booking-related session data in a structured way.
    Logs session data for debugging.
    """
    session_data = {
        'event_slug': request.session.get('event_slug'),
        'booking_id': request.session.get('booking_id'),
        'selected_event_type': request.session.get('selected_event_type'),
        'selected_tier': request.session.get('selected_tier'),
        'event_location': request.session.get('event_location', {}),
        'selected_venue': request.session.get('selected_venue', ''),
        'venue_tier': request.session.get('selected_venue_tier', ''),
    }

    logger.info(f"Session Data: {session_data}")
    return session_data


from decimal import Decimal

def calculate_total_price(customization):
    """
    Calculate the total price based on selected options, guest count, and venue tier.
    """
    base_price = Decimal('0')

    # Get the guest count
    guest_count = customization.get('guest_count', 0)

    # Venue tier pricing
    venue_tier = customization.get('venue_tier', 'Minimal')
    venue_tier_pricing = {"Minimal": Decimal('0'), "Medium": Decimal('300'), "Luxury": Decimal('600')}
    base_price += venue_tier_pricing.get(venue_tier, Decimal('0'))

    # Add-on pricing
    selected_options = customization.get('selected_options', {})
    for addon_key, addon_data in selected_options.items():
        addon_price = Decimal(addon_data.get("price", "0"))
        if addon_data.get("per_guest", False):
            base_price += addon_price * guest_count  # Price per guest
        else:
            base_price += addon_price  # Flat rate

    return base_price


import logging
from django.conf import settings

# Set up a logger to output to terminal
logger = logging.getLogger('django')
logger.setLevel(logging.DEBUG)

# Optional: You can also log to a file if you want
# logging.basicConfig(filename='session_log.txt', level=logging.DEBUG)

def log_session_data(request):
    """
    Logs all session data to the terminal and optionally saves it in a file named after session_key.
    """
    session_data = request.session.items()
    session_log = {
        "session_key": request.session.session_key,
        "session_data": dict(session_data)
    }
    logger.debug(f"Session data: {request.session.items()}")
    # Log to terminal
    logger.debug("Session Data: %s", session_log)

    # Optionally, log to a file with the session_key
    with open(f"session_{request.session.session_key}.log", 'a') as log_file:
        log_file.write(f"{session_log}\n")

    return session_log
