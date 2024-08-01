from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


async def choosing_user(user_list):
    keyboard = InlineKeyboardBuilder()
    for user in user_list:
        keyboard.add(
            InlineKeyboardButton(
                text=f"Пользователь: {user.tg_id} Админ: {user.is_staff}",
                callback_data=f"user_{user.id}",
            )
        )
    return keyboard.adjust(2).as_markup()
