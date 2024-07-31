import logging
from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, CallbackQuery

from repositories.users import get_user_by_tg_id, create_user


class AllowedUsersMiddleware(BaseMiddleware):

    async def is_user_allowed(self, user_id: int) -> bool:
        user = await get_user_by_tg_id(user_id)

        if user is None:
            await create_user(user_id)
            logging.info(f"New user, telegram_id={user_id}")
            return False

        if user.is_staff is False:
            logging.info(f"Not allowed user telegram_id={user_id}")
            return False

        return True

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:

        if await self.is_user_allowed(event.from_user.id):
            return await handler(event, data)
