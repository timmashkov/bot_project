import asyncio
import logging
from typing import Awaitable, Optional

from aiogram import Bot, Dispatcher

from infractructure.base_entities.singleton import Singleton


class Server(Singleton):
    def __init__(
        self,
        token: str,
        start_callbacks: list[Awaitable | callable] = None,
        stop_callbacks: list[Awaitable] = None,
        logging_config: Optional[str] = None,
    ) -> None:
        self.token = token
        self.logging_config = logging_config.upper() if logging_config else logging.INFO
        self.__app = Bot(token=self.token)
        self.__dispatcher = Dispatcher()
        self.start_callbacks = start_callbacks or []
        self.stop_callbacks = stop_callbacks or []

    async def run_server(self) -> None:
        await self._init_start_callbacks()
        await self._init_logger()
        await self.__dispatcher.start_polling(self.__app)

    async def _init_logger(self) -> None:
        logging.basicConfig(level=self.logging_config)
        logging.info("Инициализация logger прошла успешно")

    async def _init_start_callbacks(self):
        # Выполняем асинхронно задачи в старте
        tasks = [callback(self.__dispatcher) for callback in self.start_callbacks]
        await asyncio.gather(*tasks)
