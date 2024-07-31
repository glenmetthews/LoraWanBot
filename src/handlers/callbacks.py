import logging

from aiogram import Router, F, types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from repositories.criteria import get_criteria_list, delete_criteria
from services.api_requests import get_device_list
from keyboards.criteria_kbs import (
    device_list_kb,
    choosing_device_type_kb,
    choosing_axis_kb,
    choosing_criteria_kb,
)

from states import CriteriaCreating

router = Router()


@router.callback_query(F.data.startswith("criteria_"))
async def criteria_callback(callback: types.CallbackQuery, state: FSMContext):
    action = callback.data.split("_")[1]
    await state.clear()
    if action == "list":
        criteria_list = await get_criteria_list()

        if criteria_list:
            message = "Список активных критериев:\n"
            for row in criteria_list:
                message += (
                    f"Название: <b>{row.dev_name}</b>\n"
                    f"Серийный номер: {row.dev_eui}\n"
                    f"Диапазон критерия: {row.low_level}:{row.high_level}\n\n"
                )

            await callback.message.edit_text(
                message,
            )
        else:
            await callback.message.edit_text("Нет активных критериев")

    elif action == "create":
        device_list = await get_device_list()
        logging.info(device_list)

        await callback.message.answer(
            "Выбери устройство", reply_markup=await device_list_kb(device_list)
        )
    elif action == "delete":
        criteria_list = await get_criteria_list()
        await callback.message.answer(
            "Выберите критерий для удаления: ",
            reply_markup=await choosing_criteria_kb(criteria_list),
        )


@router.callback_query(StateFilter(None), F.data.startswith("new-cr_"))
async def new_criteria_dev_eui_callback(
    callback: types.CallbackQuery, state: FSMContext
):

    dev_eui = callback.data.split("_")[1]
    device_list = await get_device_list()

    dev_name = "Invalid Name"

    for dev in device_list:
        if dev["deveui"] == dev_eui:
            dev_name = dev["devname"]

    await state.update_data(dev_eui=dev_eui, dev_name=dev_name)
    await callback.message.answer(
        text="Выберите тип устройства: ", reply_markup=await choosing_device_type_kb()
    )
    await state.set_state(CriteriaCreating.dev_eui)


@router.callback_query(CriteriaCreating.dev_eui, F.data.startswith("device_"))
async def choosing_device_type_callback(
    callback: types.CallbackQuery, state: FSMContext
):

    device_type = callback.data.split("_")[1]

    if device_type == "nakl":
        await state.update_data(dev_type=device_type)
        await callback.message.answer(
            text="Выберите ось: ", reply_markup=await choosing_axis_kb()
        )
        await state.set_state(CriteriaCreating.criteria_axis)

    elif device_type == "disp":
        await state.update_data(dev_type=device_type, axis="displacement")
        await callback.message.answer(text="Введите диапазон. Пример: -15,5 : 35")
        await state.set_state(CriteriaCreating.criteria_range)


@router.callback_query(CriteriaCreating.criteria_axis, F.data.startswith("axis"))
async def choosing_axis_callback(callback: types.CallbackQuery, state: FSMContext):

    axis = callback.data.split("_")[1]
    await state.update_data(axis=f"tilt_{axis}")
    await callback.message.answer(text="Введите диапазон. Пример: -15,5 : 35")

    await state.set_state(CriteriaCreating.criteria_range)


@router.callback_query(StateFilter(None), F.data.startswith("delete_"))
async def delete_criteria_callback(callback: types.CallbackQuery):

    criteria_id = callback.data.split("_")[1]

    await delete_criteria(criteria_id=int(criteria_id))

    await callback.message.answer(text="Критерий удален")
