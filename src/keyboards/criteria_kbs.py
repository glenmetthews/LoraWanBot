from aiogram import types
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


async def choosing_action_with_criteria_kb():
    buttons = [
        [
            types.InlineKeyboardButton(
                text="Просмотр активных критериев", callback_data="criteria_list"
            )
        ],
        [
            types.InlineKeyboardButton(
                text="Создать критерий", callback_data="criteria_create"
            ),
        ],
        [
            types.InlineKeyboardButton(
                text="Удалить критерий", callback_data="criteria_delete"
            ),
        ],
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


async def device_list_kb(device_list):
    keyboard = InlineKeyboardBuilder()
    for device in device_list:
        keyboard.add(
            InlineKeyboardButton(
                text=device["devname"],
                callback_data=f"new-cr_{device['deveui']}",
            )
        )
    return keyboard.adjust(2).as_markup()


async def choosing_device_type_kb():
    buttons = [
        [types.InlineKeyboardButton(text="Наклономер", callback_data="device_nakl")],
        [
            types.InlineKeyboardButton(
                text="Датчик перемещения", callback_data="device_disp"
            ),
        ],
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


async def choosing_axis_kb():
    buttons = [
        [types.InlineKeyboardButton(text="Ось X", callback_data="axis_x")],
        [
            types.InlineKeyboardButton(text="Ось Y", callback_data="axis_y"),
        ],
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


async def choosing_criteria_kb(criteria_list):
    keyboard = InlineKeyboardBuilder()
    for criteria in criteria_list:
        keyboard.add(
            InlineKeyboardButton(
                text=f"{criteria.dev_name} {criteria.axis} {criteria.low_level}: {criteria.high_level}",
                callback_data=f"delete_{criteria.id}",
            )
        )
    return keyboard.adjust(2).as_markup()
