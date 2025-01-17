from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .base import CRUDBase
from app.models import Donation


class DonationCRUD(CRUDBase):

    async def get_user_donations(
            self,
            user_id: int,
            session: AsyncSession
    ) -> list[Donation]:
        db_objs = await session.execute(
            select(Donation).where(Donation.user_id == user_id)
        )
        return db_objs.scalars().all()


donation_crud = DonationCRUD(Donation)
