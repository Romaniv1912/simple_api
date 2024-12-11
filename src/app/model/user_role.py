from sqlalchemy import Column, ForeignKey, Integer, Table

from src.common.model import Base

user_role = Table(
    'user_roles',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id', ondelete='CASCADE'), primary_key=True, comment='user id'),
    Column('role_id', Integer, ForeignKey('roles.id', ondelete='CASCADE'), primary_key=True, comment='role id'),
)
