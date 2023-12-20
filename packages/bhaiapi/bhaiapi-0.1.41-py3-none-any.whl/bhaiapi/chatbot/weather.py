import requests
from bhaiapi.chatbot.open_app import speak_text
import os
def print_weather_data(api_key, location):
    base_url = "http://api.weatherstack.com/current"
    params = {"access_key": api_key, "query": location}

    try:
        response = requests.get(base_url, params=params)
        data = response.json()

        if response.status_code == 200:
            # Extract and print relevant weather information
            weather_info = data.get("current", {})
            location_info = data.get("location", {})
            temperature = weather_info.get("temperature")
            description = weather_info.get("weather_descriptions", [])[0]
            humidity = weather_info.get("humidity")
            localtime = location_info.get("localtime")
            country = location_info.get("country")
            
            speak_text(f"Weather in {location}, {country} Temperature {temperature}°C, condition {description}, Humidity {humidity}% , Observed in time {localtime}")
        else:
            speak_text(f"Failed to fetch weather data. Error: {data.get('error', {}).get('info')}")

    except Exception as e:
        print(f"An error occurred: {e}")