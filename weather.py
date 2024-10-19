from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Replace with your actual API key
API_KEY = 'api_key'

# List of Indian cities with their coordinates
cities = {
    'Delhi': (28.6139, 77.2090),
    'Mumbai': (19.0760, 72.8777),
    'Bengaluru': (12.9716, 77.5946),
    'Chennai': (13.0827, 80.2707),
    'Kolkata': (22.5726, 88.3639),
    'Hyderabad': (17.3850, 78.4867),
}

@app.route('/', methods=['GET', 'POST'])
def index():
    weather_data = {}
    if request.method == 'POST':
        selected_city = request.form.get('city')
        if selected_city:
            lat, lon = cities[selected_city]
            url = f"http://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&appid={API_KEY}"
            response = requests.get(url)
            if response.status_code == 200:
                weather_data[selected_city] = response.json()
            else:
                weather_data[selected_city] = {'error': 'Failed to fetch weather data.'}

    return render_template('index.html', weather_data=weather_data, cities=cities)

if __name__ == '__main__':
    app.run(debug=True)
