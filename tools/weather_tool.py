import os
import re
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENWEATHERMAP_API_KEY")

# Minimal normalization (only where OpenWeather fails)
CITY_ALIASES = {
    "bangalore": "bengaluru,IN",
    "bengaluru": "bengaluru,IN",
    "delhi": "delhi,IN",
    "mumbai": "mumbai,IN",
    "chennai": "chennai,IN",
    "kolkata": "kolkata,IN",
}


def extract_city(text: str) -> str:
    text = text.lower().strip()

    match = re.search(r"in\s+([a-zA-Z\s]+)", text)
    if match:
        return match.group(1).strip()

    return text


def normalize_city(city: str) -> str:
    return CITY_ALIASES.get(city, city)


def get_weather(query: str) -> str:
    if not API_KEY:
        return "❌ Weather API key missing."

    city = normalize_city(extract_city(query))

    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric",
    }

    try:
        r = requests.get(url, params=params, timeout=10)
        data = r.json()

        if r.status_code != 200:
            return f"⚠️ Weather not found for {city}."

        desc = data["weather"][0]["description"].capitalize()
        temp = data["main"]["temp"]

        return f"🌤️ {city.split(',')[0].title()}: {temp}°C, {desc}"

    except requests.exceptions.RequestException:
        return "❌ Weather service unavailable."
