from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_new_data_for_update,
    check_project_exists,
    check_project_has_investments,
    check_project_is_closed,
    check_project_name
)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import chartityproject_crud
from app.crud.donation import donation_crud
from app.schemas.charity_project import (
    CharityProjectCreate,
    CharityProjectDB,
    CharityProjectUpdate
)
from app.services.investments import make_investments


router = APIRouter()


@router.get(
    '/',
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True
)
async def get_all_projects(session: AsyncSession = Depends(get_async_session)):
    return await chartityproject_crud.get_all(session)


@router.post(
    '/',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
    response_model_exclude_none=True
)
async def create_project(
    project_data: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session)
):
    await check_project_name(project_data.name, session)
    new_project = await chartityproject_crud.create(project_data, session)
    donations = await donation_crud.get_open_objs(session)
    if donations:
        new_project = await make_investments(new_project, donations, session)
    return new_project


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
    response_model_exclude_none=True
)
async def delete_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    project = await check_project_exists(project_id, session)
    check_project_is_closed(project.fully_invested)
    check_project_has_investments(project.invested_amount)
    return await chartityproject_crud.remove(project, session)


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
    response_model_exclude_none=True
)
async def update_project(
    project_id: int,
    update_data: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session)
):
    project = await check_project_exists(project_id, session)
    await check_project_name(update_data.name, session)
    check_project_is_closed(project.fully_invested)
    check_new_data_for_update(
        update_data.full_amount, project.invested_amount
    )
    return await chartityproject_crud.update(
        project,
        update_data,
        session
    )
