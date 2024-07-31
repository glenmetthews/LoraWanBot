import logging

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from keyboards.criteria_kbs import choosing_action_with_criteria_kb
from scheduled import scheduler
from states import CriteriaCreating
from scheduled.check_criteria import check_criteria
from repositories.criteria import create_criteria

router = Router()


@router.message(F.text == "Критерии")
async def start_command(message: Message):

    await message.answer(
        text="Выбери нужное... Если осмелишься",
        reply_markup=await choosing_action_with_criteria_kb(),
    )


@router.message(
    CriteriaCreating.criteria_range,
    F.text.regexp(r"^[+-]?[0-9]+[,.]*[0-9]*\s*:\s*[+-]?[0-9]+[,.]*[0-9]*$"),
)
async def range_criteria_handler(
    message: Message, state: FSMContext, scheduler: AsyncIOScheduler
):
    user_data = await state.get_data()

    low_level, high_level = message.text.replace(",", ".").split(":")

    new_criteria = await create_criteria(
        dev_eui=user_data["dev_eui"],
        dev_name=user_data["dev_name"],
        low_level=low_level,
        high_level=high_level,
        axis=user_data["axis"],
    )
    logging.info(f"Criteria Creating: {new_criteria}")
    await state.clear()

    scheduler.add_job(
        name=user_data["dev_name"],
        func=check_criteria,
        trigger="interval",
        minutes=15,
        kwargs={"bot": message.bot, "criteria": new_criteria},
    )
    await message.answer(
        text=f"Критерий создан!",
    )


@router.message(CriteriaCreating.criteria_range)
async def invalid_low_level_criteria_handler(message: Message):
    await message.answer(
        text=f"Введи число",
    )
