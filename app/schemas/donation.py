from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, NonNegativeInt, PositiveInt

from app.extra.constants import FULL_AMOUNT_EXAMPLE_VALUE


class DonationCreate(BaseModel):
    full_amount: PositiveInt = Field(..., example=FULL_AMOUNT_EXAMPLE_VALUE)
    comment: Optional[str]

    class Config:
        anystr_strip_whitespace = True


class DonationUserDB(DonationCreate):
    id: int
    create_date: datetime

    class Config(DonationCreate.Config):
        orm_mode = True


class DonationAllDB(DonationUserDB):
    user_id: int
    invested_amount: NonNegativeInt
    fully_invested: bool
    close_date: Optional[datetime]
