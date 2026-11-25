
from services.database_service import TravelDatabaseService


class DestinationResearchAgent:

    def __init__(self):
        self.name = "Destination Research Agent"
        self.database = TravelDatabaseService()

    def get_role(self):
        return "Python-based Destination Research Specialist"

    def get_name(self):
        return self.name

    def get_response(self, user_request):

        request = user_request.lower()

        destinations = self.database.get_destinations()

        # Identify destination
        selected_destination = None

        for destination in destinations:
            name = destination["destination_name"]

            if name.lower() in request:
                selected_destination = destination
                break

        # No destination specified
        if not selected_destination:

            available_destinations = [
                d["destination_name"] for d in destinations
            ]

            return (
                "## Available Travel Destinations\n\n"
                + "\n".join(
                    f"- {name}" for name in available_destinations
                )
                + "\n\nPlease specify a destination "
                  "for detailed travel research."
            )

        destination_name = selected_destination["destination_name"]

        # Database retrieval
        hotels = self.database.get_hotels(destination_name)
        activities = self.database.get_activities(destination_name)

        # Destination information
        result = f"""
# Destination Research Report

## Destination Overview

- **Destination:** {destination_name}
- **State:** {selected_destination['state']}
- **Category:** {selected_destination['category']}
- **Description:** {selected_destination['description']}
- **Best Time to Visit:** {selected_destination['best_time_to_visit']}
- **Estimated Destination Cost:** ₹{selected_destination['estimated_cost']:,.0f}

---

## Popular Attractions & Activities
"""

        if activities:
            for activity in activities:
                result += f"""
### {activity['activity_name']}

- **Category:** {activity['category']}
- **Estimated Cost:** ₹{activity['estimated_cost']:,.0f} per person
- **Description:** {activity['description']}
"""
        else:
            result += "\nNo activity records available in database.\n"

        # Hotel recommendations
        result += "\n---\n\n## Hotel Recommendations\n"

        if hotels:
            for hotel in hotels:
                result += f"""
### {hotel['hotel_name']}

- **Location:** {hotel['address']}
- **Price:** ₹{hotel['price_per_night']:,.0f} per night
- **Rating:** {hotel['rating']}/5
"""
        else:
            result += "\nNo hotel records available.\n"

        # Travel tips
        result += """
---

## Travel Tips

- Plan your visit during the recommended travel season.
- Check weather conditions before travelling.
- Confirm hotel prices and availability before booking.
- Keep sufficient time for sightseeing and relaxation.

---


"""

        return result


if __name__ == "__main__":

    agent = DestinationResearchAgent()

    print(agent.get_response(
        "Research Goa destination and suggest hotels and activities"
    ))
