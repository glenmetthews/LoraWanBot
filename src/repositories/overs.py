from datetime import datetime

from sqlalchemy import select

from database.init_db import async_session
from database import Over, Criteria


async def create_over(criteria: Criteria, value: float, time: datetime) -> Over:
    async with async_session() as session:
        over = Over(
            criteria_id=criteria.id,
            values=value,
            time=time,
        )
        session.add(over)
        await session.flush()
        await session.commit()
        return over


async def get_over(criteria: Criteria, time: datetime) -> Over:
    async with async_session() as session:
        return await session.scalar(
            select(Over).where(Over.criteria_id == criteria.id, Over.time == time)
        )
