from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from app.utils.calculator import Calculator

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)


def critic_agent(state):
    itinerary = state["itinerary"]
    budget_review = state.get("budget_review", "No budget review provided.")

    # 🔒 ABSOLUTE SAFETY
    per_person_daily = state.get("per_person_daily", 3000)
    days = state.get("days", 1)
    people = state.get("people", 1)

    # ✅ Safe math
    per_person_total = Calculator.multiply(per_person_daily, days)
    final_total = Calculator.multiply(per_person_total, people)

    prompt = f"""
You are a senior travel planner AI.

INPUT ITINERARY:
{itinerary}

BUDGET REVIEW:
{budget_review}

LOCKED VALUES:
- Per-person daily cost: ₹{per_person_daily}
- Days: {days}
- Travelers: {people}

RULES:
- Expand each day with Morning / Afternoon / Evening
- 4–6 rich lines per day
- DAY-WISE COST VARIATION (MANDATORY):

- Base per-person daily cost = ₹{per_person_daily}

- You MUST vary daily totals:
  • Travel-heavy days (intercity trains, flights) → 10–20% HIGHER
  • Activity-heavy days (guided tours, paid attractions) → 5–15% HIGHER
  • Relaxed / local days → 5–10% LOWER

- NO two days are allowed to have the same total cost.
- Cost breakdown MUST reflect the activities of that day.

- ALWAYS show INR costs
- DO NOT repeat identical totals blindly
-If two consecutive days accidentally result in the same total,
you MUST adjust the activities cost to create a difference.


FORMAT:

### Day X: Title
**Morning:** ...
**Afternoon:** ...
**Evening:** ...

**Cost Breakdown (₹ per person):**
- Accommodation
- Food
- Local Travel
- Activities
- **Total for Day X:** ₹XXXX

FINAL:
- Calculate the PER-PERSON TOTAL by summing all day totals shown above
- FINAL TRIP COST = per-person total × number of travelers
- Show the calculation clearly in INR

"""

    response = llm.invoke(prompt)

    return {
        "final_output": response.content
    }
