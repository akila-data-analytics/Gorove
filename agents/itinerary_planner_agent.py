
import re
from services.database_service import TravelDatabaseService


class ItineraryPlannerAgent:

    def __init__(self):
        self.name = "Itinerary Planner Agent"
        self.database = TravelDatabaseService()

    def get_role(self):
        return "Python-based Travel Itinerary Planning Specialist"

    def get_name(self):
        return self.name

    def get_response(self, user_request):

        request = user_request.lower()

        # ----------------------------------
        # 1. Identify latest user message
        # ----------------------------------

        current_request_match = re.search(
            r"CURRENT USER MESSAGE:\s*(.*?)(?:\n\s*PREVIOUS USER MESSAGES|\Z)",
            user_request,
            re.IGNORECASE | re.DOTALL
        )

        if current_request_match:
            current_request = current_request_match.group(1).strip().lower()
        else:
            current_request = request

        # ----------------------------------
        # 2. Identify destination
        # ----------------------------------

        destinations = self.database.get_destinations()

        selected_destination = None

        for destination in destinations:

            name = destination["destination_name"]

            if name.lower() in request:
                selected_destination = name
                break

        if not selected_destination:
            return (
                "Please specify a destination for itinerary planning."
            )

        # ----------------------------------
        # 3. Extract trip duration
        # ----------------------------------

        # First priority: Latest user message
        day_match = re.search(
            r"\b(\d+)\s*[- ]?\s*days?\b",
            current_request
        )

        # Second priority: Previous conversation context
        if not day_match:
            day_match = re.search(
                r"\b(\d+)\s*[- ]?\s*days?\b",
                request
            )

        days = int(day_match.group(1)) if day_match else 3

        days = max(1, min(days, 14))

        # ----------------------------------
        # 4. Retrieve destination activities
        # ----------------------------------

        activities = self.database.get_activities(
            selected_destination
        )

        if not activities:
            return (
                f"No activities are available in the database "
                f"for {selected_destination}."
            )

        # ----------------------------------
        # 5. Generate itinerary
        # ----------------------------------

        result = f"""
# {days}-Day Travel Itinerary

**Destination:** {selected_destination}

**Duration:** {days} Days

---

"""

        activity_index = 0
        scheduled_activities = 0

        time_slots = [
            "Morning",
            "Afternoon",
            "Evening"
        ]

        for day in range(1, days + 1):

            result += f"\n## Day {day}\n\n"

            for time_slot in time_slots:

                if activity_index < len(activities):

                    activity = activities[activity_index]

                    result += f"""### {time_slot}: {activity['activity_name']}

- **Category:** {activity['category']}
- **Estimated Cost:** ₹{activity['estimated_cost']:,.0f} per person
- **Description:** {activity['description']}

"""

                    activity_index += 1
                    scheduled_activities += 1

                else:

                    result += f"""### {time_slot}: Leisure Time

- Relax and explore the local surroundings.
- Enjoy local food and shopping.

"""

        # ----------------------------------
        # 6. Food Recommendations
        # ----------------------------------

        result += """
---

## Food Recommendations

- Try popular local restaurants.
- Explore traditional regional dishes.
- Check restaurant reviews before visiting.

"""

        # ----------------------------------
        # 7. Travel Tips
        # ----------------------------------

        result += """
---

## Travel Tips

- Start sightseeing early to avoid crowds.
- Check weather conditions before travelling.
- Keep sufficient time for relaxation.
- Confirm activity timings before visiting.

"""

        # ----------------------------------
        # 8. Itinerary Summary
        # ----------------------------------

        remaining_activities = len(activities) - scheduled_activities

        result += f"""
---

## Itinerary Summary

- **Destination:** {selected_destination}
- **Total Days:** {days}
- **Available Database Activities:** {len(activities)}
- **Scheduled Activities:** {scheduled_activities}
- **Remaining Activities:** {remaining_activities}

"""

        return result


if __name__ == "__main__":

    agent = ItineraryPlannerAgent()

    print(
        agent.get_response(
            "Plan a 2-day trip to Ooty"
        )
    )
