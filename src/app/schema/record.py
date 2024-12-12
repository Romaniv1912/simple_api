from datetime import datetime

from pydantic import ConfigDict

from src.common.schema import SchemaBase


class RecordSchemaBase(SchemaBase):
    bot_token: str
    chat_id: str
    message: str


class CreateRecordParam(RecordSchemaBase):
    pass


class GetRecordListDetails(RecordSchemaBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_time: datetime
    updated_time: datetime | None = None
