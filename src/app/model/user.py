from typing import Union

from sqlalchemy import Boolean, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.app.model.user_role import user_role
from src.common.model import Base, id_key


class User(Base):
    """User table"""

    __tablename__ = 'users'

    id: Mapped[id_key] = mapped_column(init=False)
    username: Mapped[str] = mapped_column(String(20), unique=True, index=True, comment='user name')
    hashed_password: Mapped[str] = mapped_column(String(length=1024), nullable=False, comment='password hash')
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False, comment='enable status')
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False, comment='superuser flag')

    # User supervisor one-to-many
    supervisor_id: Mapped[int | None] = mapped_column(
        ForeignKey('users.id', ondelete='SET NULL'), default=None, comment='supervisor id'
    )
    supervisor: Mapped[Union['User', None]] = relationship('User', init=False, back_populates='users', remote_side=id)
    users: Mapped[list['User']] = relationship('User', init=False, back_populates='supervisor')

    # User role many-to-many
    roles: Mapped[list['Role']] = relationship(  # noqa: F821
        init=False, secondary=user_role, back_populates='users'
    )
