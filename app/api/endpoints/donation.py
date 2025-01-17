from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.charity_project import chartityproject_crud
from app.crud.donation import donation_crud
from app.models import User
from app.schemas.donation import (
    DonationAllDB,
    DonationCreate,
    DonationUserDB
)
from app.services.investments import make_investments


router = APIRouter()


@router.get(
    '/',
    response_model=list[DonationAllDB],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session)
):
    return await donation_crud.get_all(session)


@router.post(
    '/',
    response_model=DonationUserDB,
    response_model_exclude_none=True
)
async def make_donation(
    donation_data: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    new_donation = await donation_crud.create(donation_data, session, user)
    projects = await chartityproject_crud.get_open_objs(session)
    if projects:
        new_donation = await make_investments(new_donation, projects, session)
    return new_donation


@router.get(
    '/my',
    response_model=list[DonationUserDB],
    response_model_exclude_none=True
)
async def get_user_donations(
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session)
):
    return await donation_crud.get_user_donations(user.id, session)
