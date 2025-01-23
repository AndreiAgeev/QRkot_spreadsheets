from datetime import datetime

from sqlalchemy import Boolean, Column, Integer, DateTime
from sqlalchemy.orm import validates

from app.extra.constants import INVESTED_AMOUNT_DEFAULT, FULL_AMOUNT_MIN


class General:
    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer, default=INVESTED_AMOUNT_DEFAULT)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=datetime.now)
    close_date = Column(DateTime)

    @validates('full_amount')
    def validate_full_amount(cls, key, value):
        if value < FULL_AMOUNT_MIN:
            raise ValueError(
                'Параметр full_amount должен быть больше 0'
            )
        return value
