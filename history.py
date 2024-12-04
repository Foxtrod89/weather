from pathlib import Path
import json
from exceptions import SystemError
from datetime import datetime
from weather_formatter import format_weather
from weather_api_service import Weather
from abc import ABC, abstractmethod
from typing import TypedDict

class WeatherStorage(ABC):
    def __init__(self, filename: str):
       self._filename = filename
       self._path = Path.cwd() / self._filename
    @abstractmethod
    def save(self):
        raise NotImplementedError

class HistoryData(TypedDict):
    time: str
    data: str

class JsonStorage(WeatherStorage):
    """create instance with IO operations of WeatherStorage"""
    def __init__(self, weather: Weather):
        self._weather = weather
        super().__init__(filename='history.json')
        self._init_file()

    def _init_file(self) -> None:
        try:
            if not Path.exists(self._path):
                print(f'File {self._filename} does not exist,\
             creating it at path {self._path}')
                with open(self._filename,'x') as file:
                    file.write('[{"history":[]}]')
        except OSError:
            raise SystemError(f"Unable to make system call to {self._path}")

    def _reading_file(self, path_to_file: Path) -> list[HistoryData]:
        data = json.load(open(path_to_file,'r'))
        return data

    def _get_time_now(self) -> str:
        time = datetime.now()
        return time.strftime('%H:%M')

    def _save_file(self,json_data: str) -> None:
        with open(self._filename,'r+') as file:
            file.write(json_data)

    def save(self) -> None:
        raw_data = self._reading_file(self._path)
        raw_data.append(
                {"time":self._get_time_now(),
                 "data":format_weather(self._weather)}
                )
        processed_json = json.dumps(raw_data, indent=3)
        self._save_file(processed_json)

def save(storage: WeatherStorage) -> None:
    storage.save()
