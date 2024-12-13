from datetime import datetime

from pydantic import ConfigDict

from src.app.schema.user import GetUserInfoNoRelationDetails
from src.common.schema import SchemaBase


class RecordSchemaBase(SchemaBase):
    bot_token: str
    chat_id: str
    message: str


class CreateRecordParam(RecordSchemaBase):
    pass


class CreateRecordExtendParam(CreateRecordParam):
    user_id: int


class GetRecordListDetails(RecordSchemaBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    created_time: datetime
    updated_time: datetime | None = None


class GetRecordInfoDetails(GetRecordListDetails):
    model_config = ConfigDict(from_attributes=True)

    user: GetUserInfoNoRelationDetails
