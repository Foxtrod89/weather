import os
ROUNDING = True #to enable rounding of GPS coordinates
PRECISION = 2 #rounding precision
LANG = 'en'
UNITS = 'metric'
LIMIT = '1'
GPS_UTILITY = 'CoreLocationCLI' # GPS utility
OPEN_WEATHER_ENVVAR = "OPENWEATHER_API" # env var for OpenWeather API service

#colors:
RED = "\033[91"

class Environment:
    _key = "" 
    
    @staticmethod
    def getting_key(key: str) -> str:
        Environment._key = os.getenv(key)
        if not Environment._key:
            raise Exception("Make sure you set env OPENWEATHER_API!")
        return Environment._key
 
OPEN_WEATHER_API = Environment.getting_key(OPEN_WEATHER_ENVVAR)
OPEN_WEATHER_URL = ("https://api.openweathermap.org/data/3.0/onecall?lat={latitude}&lon={longitude}&appid="+OPEN_WEATHER_API+"&units="+UNITS+"&lang="+LANG+"&exclude=minutely,hourly,daily")
GEOCODING_URL = ("http://api.openweathermap.org/geo/1.0/reverse?lat={latitude}&lon={longitude}&limit="+LIMIT+"&appid="+OPEN_WEATHER_API+"")


