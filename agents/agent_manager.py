
import re

from agents.travel_assistant_agent import TravelAssistantAgent
from agents.destination_research_agent import DestinationResearchAgent
from agents.budget_analyst_agent import BudgetAnalystAgent
from agents.itinerary_planner_agent import ItineraryPlannerAgent
from agents.booking_assistant_agent import BookingAssistantAgent


class TravelAgentManager:

    def __init__(self):
        self.travel_agent = TravelAssistantAgent()
        self.destination_agent = DestinationResearchAgent()
        self.budget_agent = BudgetAnalystAgent()
        self.itinerary_agent = ItineraryPlannerAgent()
        self.booking_agent = BookingAssistantAgent()

        self.agents = {
            "travel_assistant": self.travel_agent,
            "destination_research": self.destination_agent,
            "budget_analyst": self.budget_agent,
            "itinerary_planner": self.itinerary_agent,
            "booking_assistant": self.booking_agent
        }

    def get_all_agents(self):
        return {
            key: agent.get_name()
            for key, agent in self.agents.items()
        }

    def contains_keyword(self, request, keywords):
        return any(keyword in request for keyword in keywords)

    def route_request(self, user_request):
        selected_agents = self.get_required_agents(user_request)
        return selected_agents[0][1]

    def get_required_agents(self, user_request):
        request = user_request.lower()
        selected_agents = []

        # 1. Destination Research Agent
        destination_keywords = [
            "destination", "places", "attractions", "sightseeing", "food",
            "beaches", "explore", "visit", "vacation", "holiday", "trip",
            "travel", "tourist", "research"
        ]

        if self.contains_keyword(request, destination_keywords):
            selected_agents.append(
                ("Destination Research Agent", self.destination_agent)
            )

        # 2. Budget Analyst Agent
        budget_keywords = [
            "budget", "cost", "expense", "price", "expenses",
            "affordable", "spending", "estimate", "estimated",
            "how much", "within", "under", "below", "limit",
            "rupees", "inr", "₹"
        ]

        has_budget_amount = bool(
            re.search(
                r"(?:₹|rs\.?|inr)\s*[\d,]+|[\d,]+\s*(?:rupees|rs\.?|inr)",
                request,
                re.IGNORECASE
            )
        )

        if (
            self.contains_keyword(request, budget_keywords)
            or has_budget_amount
        ):
            selected_agents.append(
                ("Budget Analyst Agent", self.budget_agent)
            )

        # 3. Itinerary Planner Agent
        itinerary_keywords = [
            "itinerary", "schedule", "day", "days", "daily", "plan my trip"
        ]

        if self.contains_keyword(request, itinerary_keywords):
            selected_agents.append(
                ("Itinerary Planner Agent", self.itinerary_agent)
            )

        # 4. Booking Assistant Agent
        booking_keywords = [
            "flight", "flights", "hotel", "hotels", "booking", "book",
            "reservation", "stay", "accommodation"
        ]

        if self.contains_keyword(request, booking_keywords):
            selected_agents.append(
                ("Booking Assistant Agent", self.booking_agent)
            )

        # 5. General travel request fallback
        if not selected_agents:
            selected_agents.append(
                ("Travel Assistant Agent", self.travel_agent)
            )

        return selected_agents

    @staticmethod
    def _build_contextual_request(user_request, conversation_history=None):
        """
        Build context with the latest user instruction first.

        Previous user messages are retained only as supporting context.
        Old assistant-generated reports are excluded to avoid using
        outdated values from previous responses.
        """

        if not conversation_history:
            return user_request

        previous_user_messages = []

        for message in conversation_history[-10:]:

            if not isinstance(message, dict):
                continue

            role = message.get("role", "user")
            content = str(message.get("content", "")).strip()

            if not content:
                continue

            # Only use previous user messages as historical context.
            if role == "user" and content != user_request:
                previous_user_messages.append(content)

        # Most recent previous user messages first.
        previous_user_messages.reverse()

        context_parts = [
            "You are handling a follow-up request in an ongoing travel conversation.",
            "",
            "IMPORTANT CONTEXT RULES:",
            "- The CURRENT USER MESSAGE is the highest priority.",
            "- If the user changes trip duration, use the newly requested duration.",
            "- If the user changes destination, use the newly requested destination.",
            "- Retain previous trip details when the user does not change them.",
            "- Retain the previously stated budget when the user says 'my budget'.",
            "- Do not use old values when the user has explicitly updated them.",
            "- Do not ask the user to repeat details already provided.",
            "- Do not invent prices, availability or booking confirmations.",
            "",
            "CURRENT USER MESSAGE:",
            user_request
        ]

        if previous_user_messages:
            context_parts.extend([
                "",
                "PREVIOUS USER MESSAGES (supporting context only):"
            ])

            for previous_message in previous_user_messages:
                context_parts.append(f"User: {previous_message}")

        return "\n".join(context_parts)

    def process_request(self, user_request, conversation_history=None):

        if not user_request or not user_request.strip():
            return "Please enter your travel question."

        # Routing remains based on the latest user message.
        selected_agents = self.get_required_agents(user_request)

        # Build context with latest instruction taking priority.
        contextual_request = self._build_contextual_request(
            user_request,
            conversation_history
        )

        combined_response = []

        for agent_name, agent in selected_agents:

            try:
                response = agent.get_response(contextual_request)
                combined_response.append(response)

            except Exception as error:
                combined_response.append(
                    f"Unable to generate response: {error}"
                )

        return "\n\n".join(combined_response)


if __name__ == "__main__":

    manager = TravelAgentManager()

    print("REGISTERED AGENTS:")
    print(manager.get_all_agents())

    test_request = (
        "Plan a 3-day family trip to Goa with itinerary, "
        "hotel options and estimated budget"
    )

    print("\nMULTI-AGENT TEST:")
    print(manager.process_request(test_request))
