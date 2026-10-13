import requests


class WeatherAPI:
    def __init__(self, api_key, base_url="https://api.weatherapi.com/v1"):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")

    def _request(self, endpoint, location, **params):
        try:
            response = requests.get(
                f"{self.base_url}/{endpoint}",
                params={"key": self.api_key, "q": location, **params},
                timeout=10,
            )
            response.raise_for_status()
            return response.json()
        except (requests.RequestException, ValueError, TypeError):
            return None

    def get_current_weather(self, location):
        return self._request("current.json", location)

    def get_forecast(self, location, days=3):
        if not 1 <= days <= 3:
            raise ValueError("days must be between 1 and 3")
        return self._request("forecast.json", location, days=days)


def format_current_weather(data):
    if not data:
        return ""

    location = data.get("location", {})
    current = data.get("current", {})
    condition = current.get("condition", {}).get("text", "")
    name = location.get("name", "")
    country = location.get("country", "")
    temp = current.get("temp_f", "")
    return f"{name}, {country}: {temp}°F, {condition}"


def format_forecast(data):
    if not data:
        return ""

    forecast_days = data.get("forecast", {}).get("forecastday", [])
    if not forecast_days:
        return ""

    day = forecast_days[0]
    day_data = day.get("day", {})
    condition = day_data.get("condition", {}).get("text", "")
    date = day.get("date", "")
    high_temp = day_data.get("maxtemp_f", "")
    low_temp = day_data.get("mintemp_f", "")
    return f"{date}: high {high_temp}°F, low {low_temp}°F, {condition}"
