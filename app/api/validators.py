from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import chartityproject_crud
from app.extra import constants
from app.extra.utils import now_iso
from app.models import CharityProject
from app.models.base import General


async def check_project_name(
        project_name: str,
        session: AsyncSession
):
    if await chartityproject_crud.get_by_name(project_name, session):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=constants.NOT_UNIQUE_NAME_ERROR
        )


async def check_project_exists(
        project_id: int,
        session: AsyncSession
) -> CharityProject:
    project = await chartityproject_crud.get_by_id(project_id, session)
    if project is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=constants.ERROR_404
        )
    return project


def check_project_is_closed(fully_invested: bool):
    if fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=constants.CLOSED_PROJECT_ERROR
        )


def check_project_has_investments(invested_amount: int):
    if invested_amount > 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=constants.HAS_INVESTMENTS_ERROR
        )


def check_new_data_for_update(full_amount: int, invested_amount: int):
    if full_amount and full_amount < invested_amount:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=constants.BAD_NEW_DATA_ERROR
        )


def check_obj_investments(obj: General):
    if obj.invested_amount == obj.full_amount:
        obj.fully_invested = True
        obj.close_date = now_iso()
    return obj
