from langgraph.graph import StateGraph
from typing import TypedDict

from app.agents.planner_agent import planner_agent
from app.agents.attraction_agent import attraction_agent
from app.agents.itinerary_agent import itinerary_agent
from app.agents.budget_agent import budget_agent
from app.agents.critic_agent import critic_agent


class TravelState(TypedDict):
    query: str
    plan_outline: str
    attractions: str
    itinerary: str
    budget_review: str
    daily_budget_estimate: int
    final_itinerary: str
    final_output: str
    people: int
    budget_type: str


graph = StateGraph(TravelState)

# ---- Nodes ----
graph.add_node("planner", planner_agent)
graph.add_node("attractions", attraction_agent)
graph.add_node("itinerary", itinerary_agent)
graph.add_node("budget", budget_agent)
graph.add_node("critic", critic_agent)

# ---- Entry ----
graph.set_entry_point("planner")

# ---- Correct Flow ----
graph.add_edge("planner", "attractions")
graph.add_edge("attractions", "itinerary")
graph.add_edge("itinerary", "budget")
graph.add_edge("budget", "critic")

# ---- Compile ----
travel_graph = graph.compile()
