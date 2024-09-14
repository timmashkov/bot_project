from typing import Optional

from aiogram import Dispatcher, types
from aiogram.filters import Command, CommandStart

from application.container import Container
from config import settings
from infractructure.base_entities.singleton import Singleton
from service.weather import WeatherService


class UserTextRouter(Singleton):

    @staticmethod
    async def register_handlers(
        dispatcher: Optional[Dispatcher],
        weather_client: WeatherService = Container.weather_client(),
    ):

        @dispatcher.message(CommandStart())
        async def greeting_user(message: types.Message):
            await message.answer(
                text=settings.PHRASES.start.format(message.from_user.full_name)
            )

        @dispatcher.message(Command("help"))
        async def help_user(message: types.Message):
            await message.answer(text=settings.PHRASES.help)

        @dispatcher.message(Command("weather"))
        async def how_weather(message: types.Message):
            await message.answer(text=settings.PHRASES.weather_greeting)

        @dispatcher.message(
            lambda message: message.reply_to_message
            and message.reply_to_message.text == settings.PHRASES.weather_greeting
        )
        async def get_weather(message: types.Message):
            city_name = message.text
            try:
                weather_report = await weather_client.parse_weather_data(city=city_name)
                await message.reply(text=weather_report)
            except Exception:
                await message.reply(text="Не удалось получить данные о погоде.")

        @dispatcher.message()
        async def user_texting(message: types.Message):
            await message.answer(text=settings.PHRASES.wait)
            if message.sticker:
                await message.reply_sticker(sticker=message.sticker.file_id)
            elif message.text:
                await message.answer(
                    reply_to_message_id=message.message_id,
                    text=settings.PHRASES.default_answer,
                )
