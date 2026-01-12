from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()


llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)

def itinerary_agent(state):
    attractions = state["attractions"]

    prompt = f"""
    Create a realistic day-wise itinerary using:
    {attractions}

    Rules:
    - Do not overload days
    - Balance travel and rest
    - Mention morning, afternoon, evening
    """

    response = llm.invoke(prompt)
    return {"itinerary": response.content}
