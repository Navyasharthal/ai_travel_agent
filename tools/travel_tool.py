from tools.amadeus_client import amadeus
import re
from datetime import datetime

# -----------------------------
# CONFIG
# -----------------------------
MAX_DAYS_AHEAD = 330  # Amadeus ~11 months limit

# Minimal alias map (ONLY where Amadeus truly fails)
# These are IATA CITY CODES (industry standard, not arbitrary hardcoding)
CITY_ALIASES = {
    "bangalore": "blr",
    "bengaluru": "blr",
    "delhi": "del",
    "new delhi": "del",
    "chennai": "maa",
    "mumbai": "bom",
    "kashmir": "srinagar",
    "jammu and kashmir": "srinagar",
    "ladakh": "leh",
    "kerala": "kochi",
    "goa": "goa",
}

# -----------------------------
# HELPERS
# -----------------------------
def normalize_city(city: str) -> str:
    city = city.lower().strip()
    return CITY_ALIASES.get(city, city)


def extract_travel_params(text: str):
    """
    Extract origin, destination, and date from user query.
    Example:
    "flight from chennai to mumbai on 23rd jan"
    """
    text = text.lower()

    route_match = re.search(r"from (.+?) to (.+?)( on|$)", text)
    date_match = re.search(r"on (\d{1,2})(st|nd|rd|th)? (\w+)", text)

    if not route_match or not date_match:
        return None

    origin = normalize_city(route_match.group(1))
    destination = normalize_city(route_match.group(2))

    day = int(date_match.group(1))
    month = date_match.group(3)[:3]  # march → mar

    today = datetime.today()

    try:
        date_obj = datetime.strptime(
            f"{day} {month} {today.year}", "%d %b %Y"
        )

        # If date already passed → move to next year
        if date_obj < today:
            date_obj = date_obj.replace(year=today.year + 1)

        # Amadeus date limit (~11 months)
        if (date_obj - today).days > MAX_DAYS_AHEAD:
            return "DATE_TOO_FAR"

    except Exception:
        return None

    return origin, destination, date_obj.strftime("%Y-%m-%d")


def resolve_iata(city: str) -> str:
    """
    Resolve city name or IATA city code using Amadeus.
    Tries CITY first, then AIRPORT.
    """
    # If already IATA
    if len(city) == 3 and city.isalpha():
        return city.upper()

    # CITY lookup
    response = amadeus.reference_data.locations.get(
        keyword=city,
        subType="CITY"
    )

    if response.data:
        return response.data[0]["iataCode"].upper()

    # AIRPORT fallback
    response = amadeus.reference_data.locations.get(
        keyword=city,
        subType="AIRPORT"
    )

    if response.data:
        return response.data[0]["iataCode"].upper()

    raise ValueError(f"No IATA code found for city or airport: {city}")


# -----------------------------
# MAIN TOOL FUNCTION
# -----------------------------
def get_travel_info(user_query: str) -> str:
    extracted = extract_travel_params(user_query)

    if extracted == "DATE_TOO_FAR":
        return "❌ Flights can only be searched up to ~11 months in advance."

    if not extracted:
        return (
            "❌ Please specify origin, destination, and date clearly.\n"
            "Example: flight from chennai to mumbai on 10th feb"
        )

    origin, destination, date = extracted

    print("🔥 Amadeus API CALLED")
    print(f"FROM: {origin} TO: {destination} DATE: {date}")

    try:
        origin_code = resolve_iata(origin)
        destination_code = resolve_iata(destination)

        flights = amadeus.shopping.flight_offers_search.get(
            originLocationCode=origin_code,
            destinationLocationCode=destination_code,
            departureDate=date,
            adults=1,
        )

        if not flights.data:
            return "❌ No flights found for the selected route and date."

        top = flights.data[0]
        airline = top["validatingAirlineCodes"][0]
        price = top["price"]["total"]
        currency = top["price"]["currency"]

        return (
            f"✈️ Cheapest flight from {origin.title()} to {destination.title()} ({date}):\n"
            f"Airline: {airline}\n"
            f"Price: {price} {currency}"
        )

    except Exception as e:
        try:
            return f"❌ Travel search failed.\n{e.response.result}"
        except Exception:
            return f"❌ Travel search failed. Raw error: {repr(e)}"
