from dataclasses import dataclass
from exceptions import CantGetCoordinates
from subprocess import Popen, PIPE
import config 

@dataclass(frozen=True, slots=True)
class Coordinates(): 
    latitude: float
    longitude: float

def get_coordinates() -> Coordinates:
    """grabbing GPS coordinates from CoreLocationCLI utility"""
    coordinates = _get_corelocationcli_data()  
    return _rounding(coordinates)

def _get_corelocationcli_data() -> Coordinates:
    output = get_utility_output(config.GPS_UTILITY)
    coordinates = _parse_utility_output(output)
    return coordinates

def get_utility_output(gps_utility: str) -> bytes:
    '''to fetch GPS data from your utility'''
    try:
        process = Popen([gps_utility], stdout=PIPE)
        error_code = process.wait()
        data, err = process.communicate(timeout=5)
        if err is not None or error_code!=0:    
            raise CantGetCoordinates
        process.kill()
        return data
    except FileNotFoundError:
        print(f"{gps_utility} is not installed on target system'\n"
              f"For more info \
            https://github.com/fulldecent/corelocationcli")
        exit(1)
            
def _parse_utility_output(data: bytes) -> Coordinates:
    try:
        coordinates_data_list = data.decode().strip().split()
        latitude_value = _convert_str_to_float(coordinates_data_list[0])
        longitude_value = _convert_str_to_float(coordinates_data_list[1])
    except UnicodeDecodeError:
        raise CantGetCoordinates
    return Coordinates(latitude=latitude_value, longitude=longitude_value)

def _convert_str_to_float(value: str) -> float: 
    try:
        coordinate_value = float(value)
    except ValueError:
        raise CantGetCoordinates
    return coordinate_value

def _rounding(coordinates: Coordinates) -> Coordinates:
    if not config.ROUNDING:
        return coordinates
    return Coordinates(*map(\
            lambda c: round(c,config.PRECISION),\
            [coordinates.latitude, coordinates.longitude]\
            ))
