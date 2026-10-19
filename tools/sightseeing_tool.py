import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPENTRIPMAP_API_KEY")

def get_sightseeing(city: str) -> str:
    if not API_KEY:
        return "❌ OpenTripMap API key missing."

    geo = requests.get(
        "https://api.opentripmap.com/0.1/en/places/geoname",
        params={"name": city, "apikey": API_KEY}
    )

    if geo.status_code != 200:
        return f"❌ Location not found for {city}."

    geo_data = geo.json()
    lat, lon = geo_data.get("lat"), geo_data.get("lon")
    if not lat or not lon:
        return f"❌ Coordinates not found for {city}."

    places = requests.get(
        "https://api.opentripmap.com/0.1/en/places/radius",
        params={
            "lat": lat,
            "lon": lon,
            "radius": 5000,
            "limit": 5,
            "format": "json",
            "apikey": API_KEY,
        }
    )

    if places.status_code != 200:
        return "❌ Failed to fetch sightseeing places."

    data = places.json()
    if not data:
        return f"ℹ️ No sightseeing places found in {city}."

    result = f"🗺️ Top sightseeing spots in {city}:\n"
    for place in data:
        result += f"- {place.get('name', 'Unknown')}\n"

    return result
