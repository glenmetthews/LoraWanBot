import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config import BotConfig
from handlers.callbacks import router as callbacks_router
from handlers.commands import router as commands_router
from handlers.messages import router as messages_router
from middlewares.allowed_users import AllowedUsersMiddleware
from middlewares.scheduler_mw import SchedulerMiddleware
from scheduled.check_criteria import check_criteria
from scheduled.scheduler import setup_scheduler


async def main():

    bot_config = BotConfig()

    dp = Dispatcher(storage=MemoryStorage())
    bot = Bot(
        token=bot_config.token.get_secret_value(),
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    scheduler = AsyncIOScheduler(timezone="Europe/Moscow")

    await setup_scheduler(bot=bot, scheduler=scheduler)

    dp.message.middleware(AllowedUsersMiddleware())
    dp.message.middleware(SchedulerMiddleware(scheduler=scheduler))

    dp.include_router(commands_router)
    dp.include_router(messages_router)
    dp.include_router(callbacks_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
