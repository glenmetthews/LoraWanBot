from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from keyboards.main_kb import main_kb

router = Router()


@router.message(CommandStart())
async def start_command(message: Message):

    await message.answer("Здорово!", reply_markup=await main_kb())
