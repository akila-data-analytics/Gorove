
from services.gemini_service import GeminiService
from services.database_service import TravelDatabaseService


class TravelAssistantAgent:

    def __init__(self):

        self.name = "Travel Assistant Agent"

        self.role = """
        You are the main Travel Assistant Agent
        in an AI-powered Travel Planner system.

        Your responsibilities:

        1. Understand travel requirements.
        2. Identify destinations and travel preferences.
        3. Understand budget and trip duration.
        4. Coordinate with specialized travel agents.
        5. Provide friendly travel guidance.

        Specialized agents:

        - Destination Research Agent
        - Budget Analyst Agent
        - Itinerary Planner Agent
        - Booking Assistant Agent
        """

        self.gemini = GeminiService()
        self.database = TravelDatabaseService()

    def get_role(self):
        return self.role

    def get_name(self):
        return self.name

    def local_response(self, user_request):

        request = user_request.lower()

        destinations = self.database.get_destinations()

        # Greeting responses
        greetings = ["hello", "hi", "hey", "good morning",
                     "good afternoon", "good evening"]

        if any(word in request for word in greetings):

            return """Hello! Welcome to your AI Travel Planner! 

I can help you with:

1. Destination research
2. Hotel recommendations
3. Flight search
4. Travel budget estimation
5. Day-wise itinerary planning
6. Booking assistance

Which destination would you like to explore?"""

        # List available destinations
        if any(word in request for word in [
            "available destinations",
            "list destinations",
            "which destinations",
            "where can i travel"
        ]):

            result = "# Available Travel Destinations\n\n"

            for destination in destinations:

                result += (
                    f"- **{destination['destination_name']}**, "
                    f"{destination['state']} – "
                    f"{destination['category']}\n"
                )

            return result

        # Identify destination
        selected_destination = None

        for destination in destinations:

            name = destination["destination_name"]

            if name.lower() in request:
                selected_destination = destination
                break

        if selected_destination:

            name = selected_destination["destination_name"]

            hotels = self.database.get_hotels(name)
            activities = self.database.get_activities(name)

            result = f"""# Your Travel Assistant

## Destination: {name}

- State: {selected_destination['state']}
- Category: {selected_destination['category']}
- Description: {selected_destination['description']}
- Best Time to Visit: {selected_destination['best_time_to_visit']}
- Estimated Destination Cost: ₹{selected_destination['estimated_cost']:,.0f}

## Database Information

- Hotels available in database: {len(hotels)}
- Activities available in database: {len(activities)}

## How I Can Help You

- For destination information, I can provide attractions and activities.
- For budget planning, I can estimate your trip expenses.
- For itinerary planning, I can prepare a day-wise travel plan.
- For booking assistance, I can search available database records.

Please tell me your trip duration and number of travellers
to get started.

"""

            return result

        # General fallback
        return """Welcome to your AI Travel Planner!

I can assist you with destination research, travel budgets,
itinerary planning, hotel recommendations and flight searches.

Please try a request like:

- Plan a 3-day family trip to Goa.
- Estimate budget for a 4-day Ooty trip for 2 people.
- Create a 5-day itinerary for Manali.
- Research hotels and activities in Jaipur.
- Search flights from Chennai to Delhi.

You can also ask me to list available destinations.

"""

    def get_response(self, user_request):

        try:

            # Try Gemini for conversational responses
            ai_response = self.gemini.generate_response(
                f"""
                {self.role}

                User Request:
                {user_request}

                Provide a friendly, useful and conversational
                travel response.
                """
            )

            # Check whether Gemini returned an error message
            if ai_response and isinstance(ai_response, str):

                error_keywords = [
                    "temporarily busy",
                    "unable to generate",
                    "service unavailable",
                    "quota exceeded",
                    "503",
                    "504",
                    "404 error"
                ]

                if not any(
                    keyword in ai_response.lower()
                    for keyword in error_keywords
                ):

                    return ai_response

        except Exception:
            pass

        # Gemini unavailable: use local Python logic
        return self.local_response(user_request)



if __name__ == "__main__":

    agent = TravelAssistantAgent()

    print(agent.get_response("Hello"))
