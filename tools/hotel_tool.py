from tools.amadeus_client import amadeus
from tools.travel_tool import normalize_city, resolve_iata

def find_hotels(city: str) -> str:
    try:
        city = normalize_city(city)
        city_code = resolve_iata(city)

        hotels = amadeus.shopping.hotel_offers.get(cityCode=city_code)

        if not hotels.data:
            return f"😕 No hotels found in {city.title()}."

        response = f"🏨 Top hotels in {city.title()}:\n"
        for hotel in hotels.data[:3]:
            name = hotel["hotel"]["name"]
            offer = hotel["offers"][0]
            price = offer["price"]["total"]
            currency = offer["price"]["currency"]
            response += f"- {name}: {price} {currency}\n"

        return response

    except Exception as e:
        return f"❌ Hotel search failed: {str(e)}"
