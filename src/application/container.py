from config import settings
from infractructure.base_entities.singleton import OnlyContainer, Singleton
from service.weather import WeatherService


class Container(Singleton):

    weather_client = OnlyContainer(
        WeatherService,
        host=settings.WEATHER.host,
        port=settings.WEATHER.port,
        protocol=settings.WEATHER.protocol,
        api_key=settings.WEATHER.api_key,
    )
