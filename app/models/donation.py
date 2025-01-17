from sqlalchemy import Column, Integer, ForeignKey, Text

from .base import General
from app.core.db import Base


class Donation(General, Base):
    user_id = Column(
        Integer,
        ForeignKey(
            'user.id',
            name='fk_donation_user_id_user'
        ),
    )
    comment = Column(Text)
