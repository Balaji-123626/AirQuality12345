import requests

def get_real_time_aqi(city, api_key):
    """
    Fetches real-time Air Quality from OpenWeather API for a given city.
    """
    if not api_key or api_key == "dummy":
        # Return dummy data for development without a valid API key
        return {
            "aqi": 3,
            "components": {
                "co": 250.0,
                "no2": 30.5,
                "o3": 60.2,
                "pm2_5": 15.5,
                "pm10": 20.0
            },
            "weather": {
                "temp": 28.5,
                "humidity": 65,
                "wind_speed": 4.2
            },
            "status": "Moderate",
            "co_mapped": 2.5 # Mocking CO(GT) for Prophet compatibility
        }

    try:
        # 1. Get coordinates for the city
        geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={api_key}"
        geo_res = requests.get(geo_url)
        geo_res.raise_for_status()
        geo_data = geo_res.json()

        if not geo_data:
            return {"error": "City not found"}

        lat = geo_data[0]["lat"]
        lon = geo_data[0]["lon"]

        # 2. Get Air Pollution data
        aqi_url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={api_key}"
        aqi_res = requests.get(aqi_url)
        aqi_res.raise_for_status()
        aqi_data = aqi_res.json()

        if "list" in aqi_data and len(aqi_data["list"]) > 0:
            pollution = aqi_data["list"][0]
            aqi_index = pollution["main"]["aqi"] # 1 to 5
            components = pollution["components"]
            
            # 3. Get Current Weather data
            weather_url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
            weather_res = requests.get(weather_url)
            weather_res.raise_for_status()
            weather_data = weather_res.json()
            
            weather_info = {
                "temp": weather_data.get("main", {}).get("temp", 0),
                "humidity": weather_data.get("main", {}).get("humidity", 0),
                "wind_speed": weather_data.get("wind", {}).get("speed", 0)
            }
            
            # OpenWeather AQI index: 1 = Good, 2 = Fair, 3 = Moderate, 4 = Poor, 5 = Very Poor
            # The user requested categories: 0-50 Good, 51-100 Moderate, 101-150 Poor, 151+ Dangerous
            # We map the 1-5 index to an approximate standard AQI for display
            aqi_value = map_openweather_to_standard_aqi(aqi_index)
            status = get_aqi_status(aqi_value)
            
            # Map CO to a value compatible with CO(GT) for any combination purposes
            # (In this project, we just display the real-time data separately alongside the ML prediction)
            co_mapped = components.get('co', 0) / 100.0

            return {
                "aqi": aqi_value,
                "components": components,
                "weather": weather_info,
                "status": status,
                "co_mapped": co_mapped
            }

        return {"error": "No pollution data available"}

    except Exception as e:
        return {"error": str(e)}

def map_openweather_to_standard_aqi(openweather_index):
    # Rough mapping for display purposes
    mapping = {
        1: 25,   # Good
        2: 75,   # Moderate (Fair)
        3: 125,  # Poor (Moderate in OpenWeather but Poor in user scale)
        4: 160,  # Dangerous (Poor)
        5: 200   # Dangerous (Very Poor)
    }
    return mapping.get(openweather_index, 0)

def get_aqi_status(aqi_value):
    if aqi_value <= 50:
        return "Good"
    elif aqi_value <= 100:
        return "Moderate"
    elif aqi_value <= 150:
        return "Poor"
    else:
        return "Dangerous"
