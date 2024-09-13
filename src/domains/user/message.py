from typing import Optional

from aiogram import Dispatcher, types

from application.container import Container
from infractructure.base_entities.singleton import Singleton
from service.weather import WeatherService


class UserActionRouter(Singleton):

    @staticmethod
    async def register_handlers(dispatcher: Optional[Dispatcher]):
        @dispatcher.message()
        async def user_texting(message: types.Message):
            await message.answer(text="Wait a bit")
            if message.sticker:
                await message.reply_sticker(sticker=message.sticker.file_id)
            elif message.text:
                await message.answer(reply_to_message_id=message.message_id, text="fuck you")
