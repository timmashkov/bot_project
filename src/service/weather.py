from aiohttp import ClientSession


class WeatherService:
    def __init__(
            self,
            host: str,
            port: int,
            protocol: str,
            api_key: str,
    ) -> None:
        self.host = host
        self.port = port
        self.protocol = protocol
        self.api_key = api_key
        self.client = None

    @property
    def url(self) -> str:
        return f"{self.protocol}://{self.host}/data/2.5/find"

    async def get_weather(self, city: str) -> dict:
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
