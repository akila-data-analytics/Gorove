
import re
from services.database_service import TravelDatabaseService


class BookingAssistantAgent:

    def __init__(self):

        self.name = "Booking Assistant Agent"
        self.database = TravelDatabaseService()

    def get_role(self):
        return "Python-based Travel Booking Assistant"

    def get_name(self):
        return self.name

    def get_response(self, user_request):

        request = user_request.lower()

        result = "# Travel Booking Assistance Report\n\n"

        

        # ----------------------------------
        # 1. Flight Search
        # ----------------------------------

        flight_match = re.search(
            r"\bfrom\s+(.+?)\s+to\s+(.+?)(?=\s+on\s+|\s+for\s+|\s+with\s+|\s+and\s+|$)",
            request
        )
        

        flights = []

        if flight_match:

            origin = flight_match.group(1).strip()
            destination = flight_match.group(2).strip()

            flights = self.database.search_flights(
                origin,
                destination
            )

            result += "## Flight Search Details\n\n"
            result += f"- Origin: {origin.title()}\n"
            result += f"- Destination: {destination.title()}\n\n"

            if flights:

                result += "### Available Database Flight Options\n\n"

                for flight in flights:

                    result += f"""### {flight['airline']} - {flight['flight_number']}

- Departure: {flight['departure_time']}
- Arrival: {flight['arrival_time']}
- Travel Date: {flight['travel_date']}
- Price: ₹{flight['price']:,.0f}

"""

            else:

                result += (
                    "No matching flights found in the local database.\n\n"
                )

        

        # ----------------------------------
        # 2. Hotel Search
        # ----------------------------------

        destinations = self.database.get_destinations()

        selected_destination = None

        for destination in destinations:

            name = destination["destination_name"]

            if name.lower() in request:

                selected_destination = name
                break

        hotels = []

        result += "\n## Hotel Search Details\n\n"

        if selected_destination:

            hotels = self.database.get_hotels(
                selected_destination
            )

            result += f"- Destination: {selected_destination}\n\n"

            if hotels:

                result += "###  Hotel Options\n\n"

                for hotel in hotels:

                    result += f"""### {hotel['hotel_name']}

- Location: {hotel['address']}
- Price: ₹{hotel['price_per_night']:,.0f} per night
- Rating: {hotel['rating']}/5

"""

            else:

                result += (
                    "No hotel records found for this destination.\n\n"
                )

        else:

            available = [
                d["destination_name"]
                for d in destinations
            ]

            result += (
                "Please specify a destination for hotel search.\n"
                "Available destinations: "
                + ", ".join(available)
                + "\n\n"
            )

        # ----------------------------------
        # 3. Price Comparison
        # ----------------------------------

        result += "## Price Comparison\n\n"

        if flights:

            cheapest_flight = min(
                flights,
                key=lambda f: f["price"]
            )

            result += (
                f"- Cheapest Flight: {cheapest_flight['airline']} "
                f"({cheapest_flight['flight_number']}) - "
                f"₹{cheapest_flight['price']:,.0f}\n"
            )

        if hotels:

            cheapest_hotel = min(
                hotels,
                key=lambda h: h["price_per_night"]
            )

            result += (
                f"- Cheapest Hotel: {cheapest_hotel['hotel_name']} - "
                f"₹{cheapest_hotel['price_per_night']:,.0f}/night\n"
            )

        if not flights and not hotels:

            result += "No matching price records available.\n"

        return result