from typing import List

from sqlalchemy import select, update

from database.init_db import async_session
from database import Criteria


async def get_criteria_list() -> List[Criteria]:
    async with async_session() as session:
        result = await session.scalars(
            select(Criteria).where(Criteria.is_active.is_(True))
        )
        return list(result)


async def create_criteria(
    dev_eui: str, dev_name: str, low_level: float, high_level: float, axis: str
) -> Criteria:
    async with async_session() as session:
        criteria = Criteria(
            dev_eui=dev_eui,
            dev_name=dev_name,
            low_level=low_level,
            high_level=high_level,
            axis=axis,
        )
        session.add(criteria)
        await session.flush()
        await session.commit()
        return criteria


async def delete_criteria(criteria_id: int) -> None:
    async with async_session() as session:
        stmt = (
            update(Criteria).where(Criteria.id == criteria_id).values(is_active=False)
        )
        await session.execute(stmt)
        await session.commit()
