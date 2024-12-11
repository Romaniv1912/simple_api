from datetime import datetime
from typing import Annotated

from sqlalchemy import DateTime, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, mapped_column

# Universal Mapped type primary key, needs to be added manually, refer to the following usage methods
# MappedBase -> id: Mapped[id_key]
# DataClassBase && Base -> id: Mapped[id_key] = mapped_column(init=False)
id_key = Annotated[
    int, mapped_column(primary_key=True, index=True, autoincrement=True, sort_order=-999, comment='Primary key id')
]


# Convention naming, needs to improve naming in database though SQLAlchemy
constraint_naming_conventions = {
    'ix': 'ix_%(column_0_label)s',
    'uq': 'uq_%(table_name)s_%(column_0_name)s',
    'ck': 'ck_%(table_name)s_%(constraint_name)s',
    'fk': 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',
    'pk': 'pk_%(table_name)s',
}


class DateTimeMixin:
    """Date and time Mixin data class"""

    created_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.now, sort_order=999, comment='creation time'
    )
    updated_time: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), onupdate=datetime.now, sort_order=999, comment='update time'
    )


class BaseModel(DateTimeMixin):
    pass


# Declarative base class, the original DeclarativeBase class,
# exists as the parent class of all base or data model classes
#
# `DeclarativeBase <https://docs.sqlalchemy.org/en/20/orm/declarative_config.html>`__
# `mapped_column() <https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column>`__
metadata = MetaData(naming_convention=constraint_naming_conventions)
Base = declarative_base(cls=BaseModel, metadata=metadata)
