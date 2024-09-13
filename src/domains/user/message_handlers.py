from typing import Optional

from aiogram import Dispatcher, types

from infractructure.base_entities.singleton import Singleton


class UserActionRouter(Singleton):

    @staticmethod
    async def register_handlers(dispatcher: Optional[Dispatcher]):
        @dispatcher.message()
        async def user_texting(message: types.Message):
            await message.answer(text=message.text)
