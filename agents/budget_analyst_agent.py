
import re
import math
from services.database_service import TravelDatabaseService


class BudgetAnalystAgent:

    def __init__(self):

        self.name = "Budget Analyst Agent"
        self.database = TravelDatabaseService()

        # Local estimated expenses (INR)
        self.food_per_person_per_day = 800
        self.transport_per_person = 1500
        self.other_per_person_per_day = 500

    def get_role(self):

        return "Python-based Travel Budget Analyst"

    def get_name(self):

        return self.name

    def get_response(self, user_request):

        request = user_request.lower()

        # ----------------------------------
        # 1. Separate current request
        # ----------------------------------

        current_match = re.search(
            r"CURRENT USER MESSAGE:\s*(.*?)(?:\n\s*PREVIOUS USER MESSAGES|\Z)",
            user_request,
            re.IGNORECASE | re.DOTALL
        )

        if current_match:
            current_request = current_match.group(1).strip().lower()
        else:
            current_request = request

        previous_context_match = re.search(
            r"PREVIOUS USER MESSAGES.*?:\s*(.*)",
            user_request,
            re.IGNORECASE | re.DOTALL
        )

        previous_context = (
            previous_context_match.group(1).lower()
            if previous_context_match else ""
        )

        # ----------------------------------
        # 2. Get destinations from SQLite
        # ----------------------------------

        destinations = self.database.get_destinations()

        selected_destination = None

        for destination in destinations:

            name = destination["destination_name"]

            if name.lower() in request:
                selected_destination = destination
                break

        if not selected_destination:

            available = [
                d["destination_name"] for d in destinations
            ]

            return (
                "Please specify your travel destination.\n\n"
                "Available destinations: "
                + ", ".join(available)
            )

        destination_name = selected_destination["destination_name"]

        # ----------------------------------
        # 3. Extract trip duration
        # ----------------------------------

        day_pattern = r"\b(\d+)\s*[- ]?\s*days?\b"

        day_match = re.search(
            day_pattern,
            current_request
        )

        if not day_match:

            day_match = re.search(
                day_pattern,
                previous_context
            )

        days = int(day_match.group(1)) if day_match else 3
        days = max(1, days)

        nights = max(0, days - 1)

        # ----------------------------------
        # 4. Extract number of travellers
        # ----------------------------------

        people_pattern = (
            r"\b(\d+)\s*(?:people|persons|travellers|"
            r"travelers|adults)\b"
        )

        people_match = re.search(
            people_pattern,
            current_request
        )

        if not people_match:

            people_match = re.search(
                people_pattern,
                previous_context
            )

        people = (
            int(people_match.group(1))
            if people_match else 2
        )

        people = max(1, people)

        # ----------------------------------
        # 5. Extract original total budget
        # ----------------------------------

        budget_patterns = [
            (
                r"\b(?:total\s+)?budget\b"
                r"\s*(?:of|is|:|-)?\s*"
                r"(?:₹|rs\.?|inr)?\s*([\d,]+)"
            ),
            (
                r"\b(?:within|under|below)\s+"
                r"(?:the\s+)?budget\s*(?:of)?\s*"
                r"(?:₹|rs\.?|inr)?\s*([\d,]+)"
            ),
            (
                r"(?:₹|rs\.?|inr)\s*([\d,]+)\s*"
                r"\bbudget\b"
            )
        ]

        user_budget = None

        for pattern in budget_patterns:

            budget_match = re.search(
                pattern,
                current_request,
                re.IGNORECASE
            )

            if budget_match:
                user_budget = float(
                    budget_match.group(1).replace(",", "")
                )
                break

        # If current message has no new budget,
        # retain the previous conversation budget.

        if user_budget is None:

            for pattern in budget_patterns:

                budget_match = re.search(
                    pattern,
                    previous_context,
                    re.IGNORECASE
                )

                if budget_match:
                    user_budget = float(
                        budget_match.group(1).replace(",", "")
                    )
                    break

        # ----------------------------------
        # 6. Extract additional shopping expense
        # ----------------------------------

        shopping_expense = 0

        shopping_patterns = [
            (
                r"(?:₹|rs\.?|inr)\s*([\d,]+)\s*"
                r"(?:for\s+)?shopping\b"
            ),
            (
                r"\bshopping\s*(?:of|for|:)?\s*"
                r"(?:₹|rs\.?|inr)\s*([\d,]+)"
            )
        ]

        for pattern in shopping_patterns:

            shopping_match = re.search(
                pattern,
                current_request,
                re.IGNORECASE
            )

            if shopping_match:

                shopping_expense = float(
                    shopping_match.group(1).replace(",", "")
                )
                break

        # ----------------------------------
        # 7. Retrieve hotels and activities
        # ----------------------------------

        hotels = self.database.get_hotels(destination_name)
        activities = self.database.get_activities(destination_name)

        # Select cheapest hotel from database

        if hotels:

            cheapest_hotel = min(
                hotels,
                key=lambda h: h["price_per_night"]
            )

            hotel_name = cheapest_hotel["hotel_name"]
            hotel_price = cheapest_hotel["price_per_night"]

        else:

            cheapest_hotel = None
            hotel_name = "Hotel price unavailable"
            hotel_price = 0

        # ----------------------------------
        # 8. Existing budget calculations
        # ----------------------------------

        # Calculate hotel rooms (2 people per room)

        rooms = math.ceil(people / 2)

        accommodation = (
            hotel_price * nights * rooms
        )

        # Food calculation

        food = (
            self.food_per_person_per_day * people * days
        )

        # Transportation estimate

        transport = self.transport_per_person * people

        # Activity costs from SQLite

        activity_per_person = sum(
            activity["estimated_cost"]
            for activity in activities
        )

        activity_total = activity_per_person * people

        # Other expenses

        other = (
            self.other_per_person_per_day * people * days
        )

        # Total estimated budget including shopping

        total = (
            accommodation
            + food
            + transport
            + activity_total
            + other
            + shopping_expense
        )

        per_person = total / people

        # Destination database estimate (reference only)

        destination_reference = (
            selected_destination["estimated_cost"]
        )

        # ----------------------------------
        # 9. Build expense breakdown
        # ----------------------------------

        result = f"""
# Travel Budget Analysis

**Destination:** {destination_name}

**Trip Duration:** {days} Days / {nights} Nights

**Travellers:** {people}

## Expense Breakdown

| Expense | Estimated Cost |
|---|---:|
| Accommodation | ₹{accommodation:,.0f} |
| Food | ₹{food:,.0f} |
| Transportation | ₹{transport:,.0f} |
| Activities | ₹{activity_total:,.0f} |
| Other Expenses | ₹{other:,.0f} |
"""

        if shopping_expense > 0:

            result += (
                f"| Shopping | ₹{shopping_expense:,.0f} |\n"
            )

        result += f"""| **Total Estimated Budget** | **₹{total:,.0f}** |

## Accommodation

Selected Hotel: {hotel_name}

Price per Night: ₹{hotel_price:,.0f}

Rooms Required: {rooms}

## Activities Included
"""

        if activities:

            for activity in activities:

                result += (
                    f"\n- {activity['activity_name']}: "
                    f"₹{activity['estimated_cost']:,.0f} "
                    f"per person"
                )

        else:

            result += "\nNo activity records available."

        result += f"""

## Budget Summary

Estimated Cost Per Person: ₹{per_person:,.0f}

Total Estimated Trip Cost: ₹{total:,.0f}

Destination Reference:

₹{destination_reference:,.0f} per person

"""

        if user_budget is not None:

            remaining = user_budget - total

            result += (
                f"Your Budget: ₹{user_budget:,.0f}\n"
            )

            if remaining >= 0:

                result += (
                    f"Remaining Budget: ₹{remaining:,.0f}\n\n"
                    "Your estimated trip is within budget."
                )

            else:

                result += (
                    f"Budget Shortfall: ₹{abs(remaining):,.0f}\n\n"
                    "Your estimated trip exceeds the budget."
                )

        return result


if __name__ == "__main__":

    agent = BudgetAnalystAgent()

    print(
        agent.get_response(
            "Estimate budget for a 3-day Goa trip for 4 people "
            "with a budget of 30000"
        )
    )
