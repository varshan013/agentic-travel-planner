from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)

def summary_agent(state):
    # ✅ SAFELY GET FINAL ITINERARY
    final_itinerary = state.get("final_itinerary") or state.get("itinerary")

    if not final_itinerary:
        raise ValueError("No itinerary available for summary")

    prompt = f"""
    You are a travel assistant.

    Summarize the following FINAL travel itinerary in a clean, user-friendly way.

    Include:
    - Trip highlights
    - Day-wise overview
    - Budget summary
    - Travel tips

    Final Itinerary:
    {final_itinerary}
    """

    response = llm.invoke(prompt)

    return {
        "final_output": response.content
    }
