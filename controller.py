from geopy.geocoders import Nominatim
import requests
import time


class WeatherData:
    def __init__(self, date, max_temp, min_temp, avg_temp, summary, icon, errors, city):
        self.date = date
        self.max_temp = max_temp
        self.min_temp = min_temp
        self.avg_temp = avg_temp
        self.summary = summary
        self.icon = icon
        self.errors = errors
        self.city = city


class Controller:
    WEATHERAPI_KEY = "d63a2f76ebc541d4a3e161651240412"  # Replace with your WeatherAPI key
    BASE_URL = "http://api.weatherapi.com/v1"

    def getGeocode(self, city):
        """Get latitude and longitude for a given city."""
        geolocator = Nominatim(user_agent="weather_app")
        location = geolocator.geocode(city)
        if location:
            return location
        else:
            raise ValueError("City not found")

    def getWeatherData(self, location, city):
        """Fetch weather data for a given location."""
        errors = None
        try:
            lat = str(location.latitude)
            long = str(location.longitude)

            # WeatherAPI endpoint for current weather
            url = f"{self.BASE_URL}/forecast.json?key={self.WEATHERAPI_KEY}&q={lat},{long}&days=1"
            response_raw = requests.get(url)
            response_raw.raise_for_status()  # Raise an error for bad HTTP response codes
            response = response_raw.json()

            # Extract weather data
            forecast = response.get("forecast", {}).get("forecastday", [{}])[0]
            if not forecast:
                raise ValueError("Weather data not found in the response.")

            date = forecast["date"]
            max_temp = forecast["day"]["maxtemp_c"]
            min_temp = forecast["day"]["mintemp_c"]
            avg_temp = forecast["day"]["avgtemp_c"]
            summary = forecast["day"]["condition"]["text"]
            icon = forecast["day"]["condition"]["icon"]

        except Exception as e:
            errors = f"Something went wrong: {str(e)}"
            return WeatherData("", "", "", "", "", "", errors, city)

        # Creating WeatherData object
        report = WeatherData(date, max_temp, min_temp, avg_temp, summary, icon, errors, city)

        return report
