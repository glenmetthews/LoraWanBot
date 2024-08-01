from datetime import datetime
from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from . import Base


class User(Base):
    tg_id: Mapped[int]
    is_staff: Mapped[bool] = mapped_column(default=False)


class Criteria(Base):
    dev_eui: Mapped[str]
    dev_name: Mapped[str]
    low_level: Mapped[float]
    high_level: Mapped[float]
    axis: Mapped[str] = mapped_column(nullable=True)
    is_active: Mapped[bool] = mapped_column(default=True)
    overs: Mapped[List["Over"]] = relationship(back_populates="criteria")


class Over(Base):
    values: Mapped[float]
    time: Mapped[datetime]
    criteria_id: Mapped[int] = mapped_column(ForeignKey(Criteria.id))
    criteria: Mapped[Criteria] = relationship(back_populates="overs")
