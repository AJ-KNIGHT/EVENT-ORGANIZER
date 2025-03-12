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
