from sqlalchemy import Column, Float, String, Text
from sqlalchemy.orm import validates

from .base import General
from app.core.db import Base
from app.extra.constants import (
    PROJECT_DESCRIPTION_MIN_LENGTH,
    PROJECT_NAME_MAX_LENGTH,
    PROJECT_NAME_MIN_LENGTH,
)


class CharityProject(General, Base):
    name = Column(String(PROJECT_NAME_MAX_LENGTH), nullable=False, unique=True)
    description = Column(Text, nullable=False)
    timedelta = Column(Float)

    @validates('name')
    def validate_name(cls, key, value):
        if (
            len(value) < PROJECT_NAME_MIN_LENGTH or
            len(value) > PROJECT_NAME_MAX_LENGTH
        ):
            raise ValueError(
                'Длина названия проекта должна быть'
                ' в пределах от 1 до 100 символов'
            )
        return value

    @validates('description')
    def validate_description(cls, key, value):
        if len(value) < PROJECT_DESCRIPTION_MIN_LENGTH:
            raise ValueError(
                'Добавьте описание'
            )
        return value
