from weather_api_service import Weather

def format_weather(weather: Weather)    ->str:
    """Format weather data in pretty way"""
    return (f"City: {weather.city}, {weather.state} \n"
            f"\033[91mTemperature: {weather.temperature} °C\033[0m\n"
            f"Description: {weather.weather_type.value}\n"
            f"Sunrise: {weather.sunrise.strftime('%H:%M')}\n"
            f"Sunset: {weather.sunset.strftime('%H:%M')}"
            )
