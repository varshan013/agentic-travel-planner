from langchain_openai import ChatOpenAI

from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)

def attraction_agent(state):
    plan_outline = state["plan_outline"]

    prompt = f"""
    Based on the trip plan:
    {plan_outline}

    Suggest top attractions and activities.
    Group them logically for a multi-day trip.
    """

    response = llm.invoke(prompt)
    return {"attractions": response.content}
