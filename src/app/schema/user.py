import uuid

from typing import Self

from fastapi_users import schemas
from pydantic import ConfigDict, model_validator

from src.app.schema.role import GetRoleListDetails
from src.common.schema import SchemaBase


class UserSchemaBase(SchemaBase):
    username: str
    supervisor_id: int | None = None


class CreateUserParam(schemas.BaseUserCreate, UserSchemaBase):
    pass


class UpdateUserParam(schemas.BaseUserUpdate, UserSchemaBase):
    pass


class GetUserInfoNoRelationDetails(schemas.BaseUser[int], UserSchemaBase):
    model_config = ConfigDict(from_attributes=True)

    uuid: uuid.UUID


class GetUserInfoListDetails(GetUserInfoNoRelationDetails):
    model_config = ConfigDict(from_attributes=True)

    users: list[GetUserInfoNoRelationDetails]
    roles: list[GetRoleListDetails]


class GetCurrentUserInfoDetail(GetUserInfoListDetails):
    model_config = ConfigDict(from_attributes=True)

    users: list[GetUserInfoNoRelationDetails] | list[int] | None = None
    roles: list[GetRoleListDetails] | list[str] | None = None

    @model_validator(mode='after')
    def handel(self) -> Self:
        """Work with teams and roles"""

        users = self.users
        if users:
            self.roles = [user.id for user in users]  # type: ignore

        roles = self.roles
        if roles:
            self.roles = [role.name for role in roles]  # type: ignore
        return self
