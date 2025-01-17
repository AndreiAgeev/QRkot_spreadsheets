from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, NonNegativeInt, PositiveInt

from app.extra.constants import (
    FULL_AMOUNT_EXAMPLE_VALUE,
    PROJECT_DESCRIPTION_MIN_LENGTH,
    PROJECT_NAME_MAX_LENGTH,
    PROJECT_NAME_MIN_LENGTH
)


class CharityProjectBase(BaseModel):
    name: str = Field(
        ...,
        min_length=PROJECT_NAME_MIN_LENGTH,
        max_length=PROJECT_NAME_MAX_LENGTH
    )
    description: str = Field(..., min_length=PROJECT_DESCRIPTION_MIN_LENGTH)
    full_amount: PositiveInt = Field(..., example=FULL_AMOUNT_EXAMPLE_VALUE)

    class Config:
        anystr_strip_whitespace = True


class CharityProjectCreate(CharityProjectBase):
    pass


class CharityProjectUpdate(CharityProjectBase):
    name: Optional[str] = Field(
        None,
        min_length=PROJECT_NAME_MIN_LENGTH,
        max_length=PROJECT_NAME_MAX_LENGTH
    )
    description: Optional[str] = Field(
        None,
        min_length=PROJECT_DESCRIPTION_MIN_LENGTH
    )
    full_amount: Optional[PositiveInt]

    class Config(CharityProjectBase.Config):
        extra = Extra.forbid


class CharityProjectDB(CharityProjectBase):
    id: int
    invested_amount: NonNegativeInt
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config(CharityProjectBase.Config):
        orm_mode = True
