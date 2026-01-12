from langchain_openai import ChatOpenAI
from app.utils.weather_info import get_weather
import re

from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)

def extract_city(plan_outline: str):
    """
    Try multiple safe ways to extract destination
    """
    # Try common patterns
    patterns = [
        r"Destination:\s*(.+)",
        r"trip to ([A-Za-z\s]+)",
        r"to ([A-Za-z\s]+)"
    ]

    for pattern in patterns:
        match = re.search(pattern, plan_outline, re.IGNORECASE)
        if match:
            return match.group(1).strip()

    return None  # fallback

def weather_agent(state):
    plan_outline = state["plan_outline"]

    city = extract_city(plan_outline)

    if not city:
        return {
            "weather_info": "Could not determine destination for weather analysis.",
            "weather_data": {}
        }

    weather_data = get_weather(city)

    prompt = f"""
    You are a weather-aware travel agent.

    Destination: {city}
    Real weather data:
    {weather_data}

    Tasks:
    - Explain how this weather impacts travel plans
    - Suggest itinerary adjustments
    """

    response = llm.invoke(prompt)

    return {
        "weather_info": response.content,
        "weather_data": weather_data
    }
