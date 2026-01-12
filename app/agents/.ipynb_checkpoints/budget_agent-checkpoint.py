from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from app.utils.expense_calculator import estimate_daily_expense

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)


def budget_agent(state):
    itinerary = state["itinerary"]
    plan_outline = state["plan_outline"]

    # 🔍 Detect budget type safely
    budget_type = "budget"
    outline = plan_outline.lower()

    if "luxury" in outline:
        budget_type = "luxury"
    elif "mid" in outline:
        budget_type = "mid"

    # ✅ ALWAYS dict
    daily_costs = estimate_daily_expense(budget_type)

    # ✅ ALWAYS number
    per_person_daily = sum(daily_costs.values())

    prompt = f"""
You are a budget analysis agent.

Trip details:
{plan_outline}

Itinerary:
{itinerary}

Daily cost breakdown (INR):
{daily_costs}

Per-person daily cost: ₹{per_person_daily}

Tasks:
- Check realism
- Suggest savings if needed
"""

    response = llm.invoke(prompt)

    # 🔒 CRITICAL: RETURN KEYS EXPLICITLY
    return {
        "budget_review": response.content,
        "per_person_daily": per_person_daily
    }


