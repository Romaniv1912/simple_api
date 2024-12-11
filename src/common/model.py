from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase, declared_attr


constraint_naming_conventions = {
    'ix': 'ix_%(column_0_label)s',
    'uq': 'uq_%(table_name)s_%(column_0_name)s',
    'ck': 'ck_%(table_name)s_%(constraint_name)s',
    'fk': 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',
    'pk': 'pk_%(table_name)s',
}


class Base(DeclarativeBase):
    """
    Declarative base class, the original DeclarativeBase class,
    exists as the parent class of all base or data model classes

    `DeclarativeBase <https://docs.sqlalchemy.org/en/20/orm/declarative_config.html>`__
    `mapped_column() <https://docs.sqlalchemy.org/en/20/orm/mapping_api.html#sqlalchemy.orm.mapped_column>`__
    """

    metadata: MetaData = MetaData(naming_convention=constraint_naming_conventions)

    @declared_attr.directive
    def __tablename__(self) -> str:
        return self.__name__.lower()
