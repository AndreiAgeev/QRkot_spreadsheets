from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .base import CRUDBase
from app.models import CharityProject


class CharityProjectCRUD(CRUDBase):

    async def get_by_id(
            self,
            project_id: int,
            session: AsyncSession
    ):
        return await session.get(self.model, project_id)

    async def get_by_name(
            self,
            name: str,
            session: AsyncSession
    ):
        db_obj = await session.execute(
            select(CharityProject).where(CharityProject.name == name)
        )
        return db_obj.scalars().first()

    async def remove(
            self,
            db_obj,
            session: AsyncSession
    ):
        await session.delete(db_obj)
        await session.commit()
        return db_obj

    async def update(
            self,
            db_obj,
            data,
            session: AsyncSession
    ):
        from app.api.validators import check_obj_investments
        obj_data = jsonable_encoder(db_obj)
        update_data = data.dict(exclude_unset=True)
        for key in obj_data:
            if key in update_data:
                setattr(db_obj, key, update_data[key])
        db_obj = check_obj_investments(db_obj)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def get_projects_by_completion_rate(self, session: AsyncSession):
        projects_list = await session.execute(
            select(
                CharityProject.name,
                CharityProject.timedelta,
                CharityProject.description,
            ).where(CharityProject.fully_invested == True) # noqa
            .order_by(CharityProject.timedelta)
        )
        projects_list = projects_list.all()
        return projects_list


chartityproject_crud = CharityProjectCRUD(CharityProject)
