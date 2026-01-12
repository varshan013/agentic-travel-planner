from langchain_openai import ChatOpenAI

from dotenv import load_dotenv
import os

load_dotenv()


llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)

def planner_agent(state):
    user_query = state["query"]

    prompt = f"""
    You are a travel planning agent.
    Extract key details from the user request:
    - destination
    - number of days
    - budget
    - travel style

    User request: {user_query}

    Return in bullet points.
    """

    response = llm.invoke(prompt)
    return {"plan_outline": response.content}
