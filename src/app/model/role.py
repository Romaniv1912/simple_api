from sqlalchemy import String
from sqlalchemy.dialects.postgresql import TEXT
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.app.model.user_role import user_role
from src.common.model import Base, id_key


class Role(Base):
    """Role table"""

    __tablename__ = 'roles'

    id: Mapped[id_key] = mapped_column(init=False)
    name: Mapped[str] = mapped_column(String(20), unique=True, comment='role name')
    is_active: Mapped[bool] = mapped_column(default=True, comment='role activation status')
    remark: Mapped[str | None] = mapped_column(TEXT, default=None, comment='remark')

    # Role user many-to-many
    users: Mapped[list['User']] = relationship(  # noqa: F821
        init=False, secondary=user_role, back_populates='roles', lazy=True
    )
