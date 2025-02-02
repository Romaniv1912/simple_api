from datetime import datetime
from typing import Annotated

from sqlalchemy import DateTime, MetaData
from sqlalchemy.orm import DeclarativeBase, Mapped, MappedAsDataclass, mapped_column

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


class DateTimeMixin(MappedAsDataclass):
    """Date and time Mixin data class"""

    created_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), init=False, default_factory=datetime.now, sort_order=999, comment='creation time'
    )
    updated_time: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), init=False, onupdate=datetime.now, sort_order=999, comment='update time'
    )


class MappedBase(DeclarativeBase):
    """
    Declarative base class, the original DeclarativeBase class,
    exists as the parent class of all base or data model classes

    `DeclarativeBase <https://docs.sqlalchemy.org/en/20/orm/declarative_config.html>`__
    `mapped_column() <https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column>`__
    """

    metadata = MetaData(naming_convention=constraint_naming_conventions)


class DataClassBase(MappedAsDataclass, MappedBase):
    """
    Declarative data class base class, which will come with data class integration, allowing more advanced configuration,
    but you must pay attention to some of its characteristics, especially when used with DeclarativeBase

    `MappedAsDataclass <https://docs.sqlalchemy.org/en/20/orm/dataclasses.html#orm-declarative-native-dataclasses>`__
    """  # noqa: E501

    __abstract__ = True


class Base(DataClassBase, DateTimeMixin):
    """
    Declarative Mixin data class base class, with data class integration, and contains MiXin data class basic table structure,
    you can simply understand it as a data class base class containing basic table structure
    """  # noqa: E501

    __abstract__ = True
