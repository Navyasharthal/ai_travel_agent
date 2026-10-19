from tools.amadeus_client import amadeus
from tools.travel_tool import extract_travel_params, resolve_iata


def estimate_budget(user_query: str) -> str:
    extracted = extract_travel_params(user_query)

    if not extracted:
        return "❌ Please specify origin, destination, and date.\nExample: flight from chennai to mumbai on 10th feb"

    origin, destination, date = extracted

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
            return "❌ No flights found for budget estimation."

        price = flights.data[0]["price"]["total"]
        currency = flights.data[0]["price"]["currency"]

        return (
            f"💰 Estimated budget from {origin.title()} to {destination.title()}:\n"
            f"{price} {currency}"
        )

    except Exception as e:
        return f"❌ Budget estimation failed: {str(e)}"
