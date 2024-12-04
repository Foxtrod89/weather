class CantGetCoordinates(Exception):
    """Unable to get coordinates"""

class ApiServiceError(Exception):
    """Program can not get api data from service OpenWeather"""

class SystemError(Exception):
    """Program has issues with system calls"""
