import asyncio

from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from scheduled.check_criteria import check_criteria
from repositories.criteria import get_criteria_list


async def setup_scheduler(bot: Bot, scheduler: AsyncIOScheduler):

    criteria_list = await get_criteria_list()

    for criteria in criteria_list:
        await asyncio.sleep(5)
        scheduler.add_job(
            name=criteria.dev_name,
            func=check_criteria,
            trigger="interval",
            minutes=1,
            kwargs={"bot": bot, "criteria": criteria},
        )

    scheduler.start()
