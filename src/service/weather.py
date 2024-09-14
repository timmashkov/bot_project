import logging
from typing import Optional

from aiohttp import ClientSession
from pydantic import ValidationError

from domains.weather.schema import WeatherResponse


class WeatherService:
    def __init__(
        self,
        host: str,
        port: int,
        protocol: str,
        api_key: str,
        logging_config: Optional[str] = None,
    ) -> None:
        self.host = host
        self.port = port
        self.protocol = protocol
        self.api_key = api_key
        self.logger = logging_config.upper() if logging_config else logging.INFO
        self.client = None

    @property
    def url(self) -> str:
        return f"{self.protocol}://{self.host}/data/2.5/find"

    @classmethod
    async def __forecast_formatter(cls, weather_response: WeatherResponse) -> str:
        city_weather = weather_response.list[0]
        city = city_weather.name
        temp = city_weather.main.temp
        feels_like = city_weather.main.feels_like
        weather = city_weather.weather[0].description
        wind_speed = city_weather.wind.speed
        pressure = city_weather.main.pressure
        humidity = city_weather.main.humidity
        rain = city_weather.rain.get("1h", "нет") if city_weather.rain else "нет"
        snow = city_weather.snow.get("1h", "нет") if city_weather.snow else "нет"

        return f"""
                Прогноз погоды в городе {city}
                Сейчас температура {temp}°C
                Ощущается как {feels_like}°
                ⛅️ {weather.capitalize()} ⛅️
                💨 Скорость ветра {wind_speed} м/с 💨
                Давление {pressure} мм рт.ст.
                Влажность {humidity}%
                💦 Дождь: {rain}
                ❄️ Снег: {snow}
                """

    async def _get_weather(self, city: str) -> dict:
        params: dict = {
            "q": city,
            "type": "like",
            "units": "metric",
            "lang": "ru",
            "APPID": self.api_key,
        }
        self.client = ClientSession(raise_for_status=True)
        async with self.client.get(self.url, params=params) as response:
            result = await response.json()
        return result

    async def parse_weather_data(self, city: str) -> Optional[str]:
        try:
            data = await self._get_weather(city=city)
            weather_response = WeatherResponse(**data)
            return await self.__forecast_formatter(weather_response=weather_response)
        except ValidationError:
            return None
