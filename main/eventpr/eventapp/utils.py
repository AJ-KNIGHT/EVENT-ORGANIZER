import requests

def get_coordinates(location):
    url = f"https://nominatim.openstreetmap.org/search?q={location}&format=json"
    response = requests.get(url)
    data = response.json()
    
    if data:
        latitude = data[0]["lat"]
        longitude = data[0]["lon"]
        return latitude, longitude
    return None, None
