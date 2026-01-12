import requests
import os

def get_weather(city: str):
    """
    Fetch current weather info for a city using OpenWeather API
    """
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        return "Weather API key not set."

    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"
    }

    try:
        res = requests.get(url, params=params, timeout=10)
        data = res.json()

        if res.status_code != 200:
            return f"Weather data not available for {city}"

        weather_desc = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]

        return {
            "description": weather_desc,
            "temperature_c": temp,
            "humidity": humidity
        }
    except Exception as e:
        return f"Weather fetch error: {str(e)}"
