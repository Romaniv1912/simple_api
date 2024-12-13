from fastapi import BackgroundTasks, Depends
from sqlalchemy import Select

from cerbos.response.v1.response_pb2 import PlanResourcesResponse
from src.app.crud.record import record_dao
from src.app.model import User
from src.app.model.record import Record
from src.app.schema.record import CreateRecordExtendParam, CreateRecordParam
from src.database import async_db_session
from src.utils.telegram import send_message
from src.utils.user import get_current_user


class RecordService:
    @staticmethod
    def get_select(plan: PlanResourcesResponse) -> Select:
        return record_dao.get_list(plan)

    @staticmethod
    async def create(obj: CreateRecordParam, bg: BackgroundTasks, user: User = Depends(get_current_user)) -> Record:
        try:
            obj.__class__ = CreateRecordExtendParam
            obj.user_id = user.id
            async with async_db_session.begin() as db:
                record = await record_dao.create(db, obj)
        except:
            raise
        else:
            bg.add_task(record_service.create_feedback, record.id, obj)

        return record

    @staticmethod
    async def create_feedback(pk: int, obj: CreateRecordParam):
        resp = await send_message(obj.bot_token, obj.chat_id, obj.message)

        async with async_db_session.begin() as db:
            await record_dao.set_response(db, pk, resp)


record_service = RecordService()
