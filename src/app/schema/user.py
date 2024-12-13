from datetime import datetime

from pydantic import ConfigDict, model_validator

from src.app.schema.role import GetRoleListDetails
from src.common.schema import SchemaBase


class AuthLoginParam(SchemaBase):
    username: str
    password: str | None


class UserSchemaBase(SchemaBase):
    username: str
    supervisor_id: int | None = None
    is_active: bool | None = True
    is_superuser: bool | None = False


class GetUserInfoNoRelationDetails(UserSchemaBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_time: datetime
    updated_time: datetime | None = None


class GetUserInfoListDetails(GetUserInfoNoRelationDetails):
    model_config = ConfigDict(from_attributes=True)

    users: list[GetUserInfoNoRelationDetails]
    roles: list[GetRoleListDetails]


class GetCurrentUserInfoDetail(GetUserInfoListDetails):
    model_config = ConfigDict(from_attributes=True)

    supervisor: GetUserInfoNoRelationDetails | None = None
    users: list[GetUserInfoNoRelationDetails] | list[int] | None = None
    roles: list[GetRoleListDetails] | list[str] | None = None

    @model_validator(mode='after')
    def handel(self):
        """Work with teams and roles"""

        users = self.users
        if users:
            self.users = [user.id for user in users]  # type: ignore

        roles = self.roles
        if roles:
            self.roles = [role.name for role in roles]  # type: ignore
        return self
