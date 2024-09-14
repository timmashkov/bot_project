from typing import List, Optional

from pydantic import BaseModel


class WeatherDescription(BaseModel):
    id: int
    main: str
    description: str
    icon: str


class Coordinates(BaseModel):
    lat: float
    lon: float


class MainWeather(BaseModel):
    temp: float
    feels_like: float
    temp_min: float
    temp_max: float
    pressure: int
    humidity: int
    sea_level: Optional[int]
    grnd_level: Optional[int]


class Wind(BaseModel):
    speed: float
    deg: int


class Clouds(BaseModel):
    all: int


class CityWeather(BaseModel):
    id: int
    name: str
    coord: Coordinates
    main: MainWeather
    wind: Wind
    clouds: Clouds
    weather: List[WeatherDescription]
    sys: dict
    rain: Optional[dict] = None
    snow: Optional[dict] = None


class WeatherResponse(BaseModel):
    message: str
    cod: str
    count: int
    list: List[CityWeather]
