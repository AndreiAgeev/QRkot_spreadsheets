from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User


class CRUDBase:

    def __init__(self, model):
        self.model = model

    async def get_all(self, session: AsyncSession):
        db_objs = await session.execute(select(self.model))
        return db_objs.scalars().all()

    async def create(
            self,
            new_object,
            session: AsyncSession,
            user: Optional[User] = None
    ):
        data = new_object.dict()
        data['close_date'] = None
        if user is not None:
            data['user_id'] = user.id
        db_obj = self.model(**data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def get_open_objs(self, session: AsyncSession):
        db_objs = await session.execute(
            select(self.model)
            .where(self.model.fully_invested == False) # noqa
            .order_by(self.model.id)
        )
        return db_objs.scalars().all()
