from sqlalchemy import select

from database.init_db import async_session
from database import User


async def get_user_by_tg_id(tg_id: int) -> User:
    """
    Get user by tg_id
    :param tg_id: Telegram user ID.
    :return: User model
    """
    async with async_session() as session:
        return await session.scalar(select(User).where(User.tg_id == tg_id))  # type: ignore


async def create_user(user_id: int) -> User:
    async with async_session() as session:
        user = User(
            tg_id=user_id,
        )
        session.add(user)
        await session.commit()
        return user


async def get_allowed_users():
    async with async_session() as session:
        result = await session.scalars(select(User).where(User.is_staff.is_(True)))
        return result
