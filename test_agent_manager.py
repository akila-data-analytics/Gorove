
from agents.agent_manager import TravelAgentManager

manager = TravelAgentManager()

print("REGISTERED AGENTS:")
print(manager.get_all_agents())

print("\nREQUEST ROUTING TEST:")

requests = [
    "Plan my travel budget",
    "Create a 3 days itinerary",
    "Find flight and hotel booking",
    "Suggest destination places",
    "Plan my international trip"
]

for request in requests:
    agent = manager.route_request(request)
    print(f"{request} -> {agent.get_name()}")
