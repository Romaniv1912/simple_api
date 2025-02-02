from datetime import datetime

from cerbos_sqlalchemy import get_query
from sqlalchemy import Select, desc, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from sqlalchemy_crud_plus import CRUDPlus

from cerbos.sdk.model import PlanResourcesResponse
from src.app.model import Record
from src.app.schema.record import CreateRecordExtendParam


class CRUDRecord(CRUDPlus[Record]):
    async def get(self, db: AsyncSession, pk: int) -> Record:
        return await self.select_model(db, pk)

    async def get_with_relation(self, db: AsyncSession, pk: int) -> Record:
        stmt = select(self.model).options(joinedload(self.model.user)).filter(self.model.id == pk)

        record = await db.execute(stmt)
        return record.scalars().first()

    def get_list(self, plan: PlanResourcesResponse) -> Select:
        """
        Get record select by plan

        :param plan:
        :return:
        """
        query = get_query(
            plan,
            self.model,  # type: ignore
            {
                'request.resource.attr.user_id': Record.user_id,
            },
        ).order_by(desc(self.model.created_time))

        return query

    async def create(self, db: AsyncSession, obj: CreateRecordExtendParam) -> Record:
        """
        Create new record

        :param db:
        :param obj:
        :return:
        """
        return await self.create_model(db, obj)

    async def set_response(self, db: AsyncSession, pk: int, response: str):
        """
        Set response for record

        :param db:
        :param pk:
        :param response:
        :return:
        """
        await self.update_model(db, pk, {'sent_response': response, 'sent_time': datetime.now()})


record_dao: CRUDRecord = CRUDRecord(Record)
