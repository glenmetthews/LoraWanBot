from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


async def main_kb():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="Критерии"),
                KeyboardButton(text="Сервисная информация"),
            ],
        ],
        resize_keyboard=True,
    )
    return keyboard
