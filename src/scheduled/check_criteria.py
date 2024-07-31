import logging
from datetime import datetime, timedelta

from aiogram import Bot

from database import Criteria
from repositories.users import get_allowed_users
from services.api_requests import get_last_tilt_data


async def check_criteria(bot: Bot, criteria: Criteria):

    allowed_users = await get_allowed_users()

    to_timestamp = int(datetime.now().timestamp() * 1000)
    from_timestamp = to_timestamp - 900 * 1000

    if criteria.axis == "tilt_x" or criteria.axis == "tilt_y":

        data = await get_last_tilt_data(
            dev_eui=criteria.dev_eui,
            from_timestamp=from_timestamp,
            to_timestamp=to_timestamp,
        )

        if not (criteria.low_level < data[criteria.axis] < criteria.high_level):
            for user in allowed_users:
                await bot.send_message(
                    text=f"{criteria.dev_name} вышел из диапазона [{criteria.low_level} - {criteria.high_level}].\n"
                    f"Время: {datetime.fromisoformat(data['time'].replace('Z', '')) + timedelta(hours=3)}\n"
                    f"Значение: {data[criteria.axis]}\n ",
                    chat_id=user.tg_id,
                )
            logging.info("Превышение")

    else:
        logging.info("Чисто")
