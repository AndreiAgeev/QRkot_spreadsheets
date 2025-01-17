from typing import Union

from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import check_obj_investments
from app.models import CharityProject, Donation


async def make_investments(
        sole_obj: Union[CharityProject, Donation],
        obj_list: list[Union[CharityProject, Donation]],
        session: AsyncSession
):
    for obj in obj_list:
        sole_obj_invests = sole_obj.full_amount - sole_obj.invested_amount
        obj_invests = obj.full_amount - obj.invested_amount
        if sole_obj_invests >= obj_invests:
            sole_obj.invested_amount += obj_invests
            obj.invested_amount += obj_invests
        if sole_obj_invests < obj_invests:
            sole_obj.invested_amount += sole_obj_invests
            obj.invested_amount += sole_obj_invests
        sole_obj = check_obj_investments(sole_obj)
        obj = check_obj_investments(obj)
        session.add_all((sole_obj, obj))
        if sole_obj.fully_invested:
            break
    await session.commit()
    await session.refresh(sole_obj)
    return sole_obj
