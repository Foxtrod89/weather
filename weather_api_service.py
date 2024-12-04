from exceptions import ApiServiceError
from enum import Enum
from datetime import datetime
from dataclasses import dataclass
from coordinates import Coordinates
from typing import TypeAlias, Literal
import urllib.request
from urllib.error import URLError
import ssl
import json
from json import JSONDecodeError 
import config

Celsius: TypeAlias = int

class WeatherType(Enum):
    THUNDERSTORM = 'Thunderstorm'
    DRIZZLE = 'Drizzling'
    RAIN = 'Raining'
    SNOW = 'Snowing'
    CLEAR = 'Clear'
    ATMOSPHERE = 'Foggy'
    CLOUDS = 'Cloudy'

@dataclass(frozen=True, slots=True)
class Weather():
    temperature : Celsius
    weather_type: WeatherType
    sunrise: datetime
    sunset: datetime
    city: str
    state: str

def get_weather(coordinates: Coordinates)-> Weather:
    """get weather from OpenWeather"""
    get_openweather_output = _get_openweather_response(latitude=coordinates.latitude, longitude=coordinates.longitude)
    get_geocoding_output = _get_geocoding_response(latitude=coordinates.latitude, longitude=coordinates.longitude)
    weather = _parse_openweather_response(get_openweather_output, geocoding_response=get_geocoding_output)
    return weather

def _get_openweather_response(latitude: float, longitude: float) -> bytes:
    ssl._create_default_https_context = ssl._create_unverified_context
    url = config.OPEN_WEATHER_URL.format(latitude=latitude, longitude = longitude)
    try:
        return urllib.request.urlopen(url).read()
    except URLError:
        raise ApiServiceError

#Call for OpenWeather GeoCoding API endpoint
def _get_geocoding_response(latitude: float, longitude: float) -> bytes:
    ssl._create_default_https_context = ssl._create_unverified_context
    url = config.GEOCODING_URL.format(latitude=latitude, longitude = longitude)
    try:
        return urllib.request.urlopen(url, timeout=3).read()
    except URLError:
        raise ApiServiceError

def _parse_openweather_response(open_weather_response: bytes, geocoding_response: bytes) -> Weather:
    try:
        open_weather_dict = json.loads(open_weather_response)
        geocoding_list = json.loads(geocoding_response)
    except JSONDecodeError:
        raise ApiServiceError
    return Weather(
        weather_type=_parse_weather_type(open_weather_dict),
        temperature=_parse_temperature(open_weather_dict),
        sunrise=_parse_unixtime(open_weather_dict,'sunrise'),
        sunset = _parse_unixtime(open_weather_dict,'sunset'),
        city=_parse_city(geocoding_list),
        state=_parse_state(geocoding_list))

def _parse_weather_type(openweather_response_dict: dict) -> WeatherType:
    try:
        weather_type_id = str(openweather_response_dict['current']['weather'][0]['id'])
    except (KeyError, IndexError):
        raise ApiServiceError
    
    weather_types = {
        "1": WeatherType.THUNDERSTORM,
        "3": WeatherType.DRIZZLE,
        "5": WeatherType.RAIN,
        "6": WeatherType.SNOW,
        "7": WeatherType.ATMOSPHERE,
        "800": WeatherType.CLEAR,
        "80": WeatherType.CLOUDS
    }
    for _id, _weather_type in weather_types.items():
        if weather_type_id.startswith(_id):
            return _weather_type
    raise ApiServiceError 

def _parse_temperature(openweather_response_dict: dict) -> Celsius:
    return openweather_response_dict['current']['temp']

def _parse_unixtime(
        openweather_response_dict: dict,
        time: Literal["sunrise"]| Literal["sunset"]
                    ) -> datetime:
    return datetime.fromtimestamp(openweather_response_dict['current'][time])

def _parse_city(geocoding_response: list) -> str:
    city = geocoding_response[0]['local_names']['en']
    return city

def _parse_state(geocoding_response: list) -> str:
    state = geocoding_response[0]['state']
    return state
