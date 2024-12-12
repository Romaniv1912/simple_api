from datetime import datetime

from pydantic import ConfigDict

from src.common.schema import SchemaBase


class RoleSchemaBase(SchemaBase):
    name: str
    is_active: bool = True
    remark: str | None = None


class GetRoleListDetails(RoleSchemaBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_time: datetime
    updated_time: datetime | None = None
