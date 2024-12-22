import requests
import os
from openai import ChatCompletion

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


def get_weather_data(city: str = "New York") -> dict:
    """
    Fetch weather data for a given city using the weather API.
    
    Args:
        city (str): City name. Defaults to "New York".
    
    Returns:
        dict: Weather data or error message.
    """
    try:
        url = f"http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={city}"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    
    except requests.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return {"error": "Unable to fetch weather data"}


def generate_weather_response(weather_data: dict) -> str:
    """
    Generate a natural language response for the weather data using GPT-4o.
    
    Args:
        weather_data (dict): Weather data from the API.
    
    Returns:
        str: Generated natural language response.
    """
    try:
        if "error" in weather_data:
            return "Unable to retrieve weather information at the moment."

        # Extract relevant weather information
        location = weather_data["location"]["name"]
        temp_c = weather_data["current"]["temp_c"]
        condition = weather_data["current"]["condition"]["text"]
        humidity = weather_data["current"]["humidity"]
        wind_kph = weather_data["current"]["wind_kph"]

        # Create a structured prompt
        prompt = (
            f"Generate a weather report for {location}:\n\n"
            f"Temperature: {temp_c}°C\n"
            f"Condition: {condition}\n"
            f"Humidity: {humidity}%\n"
            f"Wind Speed: {wind_kph} kph\n"
        )

        # Send the prompt to GPT-4o
        response = ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a weather assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=100,
            temperature=0.7
        )

        return response["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"Error generating weather response: {e}")
        return "Unable to generate a weather response at the moment."
