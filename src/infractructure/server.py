import logging
from typing import Optional

from aiogram import Bot, Dispatcher

from infractructure.base_entities.singleton import Singleton


class Server(Singleton):
    def __init__(
        self,
        token: str,
        start_callbacks: list[callable] = None,
        stop_callbacks: list[callable] = None,
        logging_config: Optional[str] = None,
    ) -> None:
        self.token = token
        self.logging_config = logging_config.upper() if logging_config else logging.INFO
        self._app = Bot(token=self.token)
        self._dispatcher = Dispatcher()
        self.start_callbacks = start_callbacks or []
        self.stop_callbacks = stop_callbacks or []

    async def run_server(self) -> None:
        await self._init_logger()
        await self._dispatcher.start_polling(self._app)

    async def _init_logger(self) -> None:
        logging.basicConfig(level=self.logging_config)
        logging.info("Инициализация logger прошла успешно")
