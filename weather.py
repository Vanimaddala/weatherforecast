
from flask import Flask, render_template, jsonify
import requests
import pandas as pd
from datetime import datetime
import os

app = Flask(__name__)

API_KEY = '77062f0771e8b4beecfbab171e6da028'  # Replace with your actual API key
LOCATIONS = {
    "Delhi": (28.6139, 77.2090),
    "Mumbai": (19.0760, 72.8777),
    "Chennai": (13.0827, 80.2707),
    "Bangalore": (12.9716, 77.5946),
    "Kolkata": (22.5726, 88.3639),
    "Hyderabad": (17.3850, 78.4867),
}

# Fetch weather data from OpenWeatherMap API
def fetch_weather_data(lat, lon):
    url = f"http://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&appid={API_KEY}&exclude=hourly,daily"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching data: {response.status_code}")
        return None

# Calculate daily summary from weather data
def calculate_daily_summary(weather_data):
    if weather_data:
        temp = weather_data['current']['temp'] - 273.15  # Convert from Kelvin to Celsius
        feels_like = weather_data['current']['feels_like'] - 273.15
        main_weather = weather_data['current']['weather'][0]['main']
        timestamp = datetime.fromtimestamp(weather_data['current']['dt']).strftime('%Y-%m-%d %H:%M:%S')

        return {
            "temperature": temp,
            "feels_like": feels_like,
            "weather": main_weather,
            "timestamp": timestamp
        }
    return None

@app.route('/')
def index():
    weather_summaries = []
    for city, coords in LOCATIONS.items():
        weather_data = fetch_weather_data(*coords)
        summary = calculate_daily_summary(weather_data)
        if summary:
            weather_summaries.append({"city": city, **summary})
    return render_template('index.html', weather_summaries=weather_summaries)

@app.route('/api/weather')
def weather_api():
    weather_summaries = []
    for city, coords in LOCATIONS.items():
        weather_data = fetch_weather_data(*coords)
        summary = calculate_daily_summary(weather_data)
        if summary:
            weather_summaries.append({"city": city, **summary})
    return jsonify(weather_summaries)

if __name__ == '__main__':
    app.run(debug=True)
