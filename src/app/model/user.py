from typing import Union
from uuid import UUID, uuid4

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.app.model.user_role import user_role
from src.common.model import Base, id_key


class User(SQLAlchemyBaseUserTable[int], Base):
    """User table"""

    __tablename__ = 'users'

    id: Mapped[id_key] = mapped_column()
    uuid: Mapped[UUID] = mapped_column(postgresql.UUID, default=uuid4, unique=True)
    username: Mapped[str] = mapped_column(String(20), unique=True, index=True, comment='user name')

    # User supervisor one-to-many
    supervisor_id: Mapped[int | None] = mapped_column(
        ForeignKey('users.id', ondelete='SET NULL'), default=None, comment='supervisor id'
    )
    supervisor: Mapped[Union['User', None]] = relationship('User', backref='users', remote_side=id)

    # User role many-to-many
    roles: Mapped[list['Role']] = relationship(  # noqa: F821
        secondary=user_role, back_populates='users'
    )
