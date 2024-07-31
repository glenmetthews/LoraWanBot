from aiogram.fsm.state import StatesGroup, State


class CriteriaCreating(StatesGroup):
    dev_eui = State()
    device_type = State()
    criteria_axis = State()
    criteria_range = State()
