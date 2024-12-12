from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy_crud_plus import CRUDPlus

from src.app.model import User


class CRUDUser(CRUDPlus[User]):
    async def get(self, db: AsyncSession, user_id: int) -> User | None:
        """
        Get user

        :param db:
        :param user_id:
        :return:
        """
        return await self.select_model(db, user_id)

    async def get_by_username(self, db: AsyncSession, username: str) -> User | None:
        """
        Get user by username

        :param db:
        :param username:
        :return:
        """
        return await self.select_model_by_column(db, username=username)

    async def get_by_nickname(self, db: AsyncSession, nickname: str) -> User | None:
        """
        Get user by nickname

        :param db:
        :param nickname:
        :return:
        """
        return await self.select_model_by_column(db, nickname=nickname)

    async def get_with_relation(self, db: AsyncSession, *, user_id: int = None, username: str = None) -> User | None:
        """
        Get user and (team, role, menu)

        :param db:
        :param user_id:
        :param username:
        :return:
        """
        stmt = select(self.model).options(selectinload(self.model.users)).options(selectinload(self.model.roles))
        filters = []
        if user_id:
            filters.append(self.model.id == user_id)
        if username:
            filters.append(self.model.username == username)
        user = await db.execute(stmt.where(*filters))
        return user.scalars().first()


user_dao: CRUDUser = CRUDUser(User)
