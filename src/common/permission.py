import abc

from typing import Callable, Generic, Type, TypeVar

from asgi_correlation_id import correlation_id
from fastapi import HTTPException, Request
from fastapi.params import Depends

from cerbos.sdk.client import AsyncCerbosClient
from cerbos.sdk.model import PlanResourcesResponse, Principal, Resource, ResourceDesc
from src.app.model import User
from src.core.conf import settings
from src.utils.user import get_current_user

TModel = TypeVar('TModel')


def get_action(request: Request):
    action = {'GET': 'read', 'POST': 'create', 'PUST': 'update', 'PATCH': 'update', 'DELETE': 'delete'}.get(
        request.method
    )

    if action is None:
        raise HTTPException(403, 'Not Allowed Method')

    return action


def get_principal(user: User = Depends(get_current_user)) -> Principal:
    attr = {'id': user.id}

    if user.users:
        attr['users'] = {user.id for user in user.users}

    return Principal(id=str(user.username), roles={role.name.lower() for role in user.roles}, attr=attr)


async def get_cerbos_client() -> AsyncCerbosClient:
    async with AsyncCerbosClient(settings.CERBOS.http_url) as client:
        yield client


class BasePermission(Generic[TModel]):
    def __init__(self, model: Type[TModel]) -> None:
        self.model = model

    @property
    def kind(self):
        return self.model.__name__.lower()

    @abc.abstractmethod
    async def __call__(
        self,
        action: str = Depends(get_action),
        p: Principal = Depends(get_principal),
        c: AsyncCerbosClient = Depends(get_cerbos_client),
    ):
        raise NotImplementedError()


class PlanPermission(BasePermission[TModel]):
    def get_resource(self) -> ResourceDesc:
        return ResourceDesc(self.kind)

    async def __call__(
        self,
        action: str = Depends(get_action),
        p: Principal = Depends(get_principal),
        c: AsyncCerbosClient = Depends(get_cerbos_client),
    ) -> PlanResourcesResponse:
        pr = self.get_resource()

        plan: PlanResourcesResponse = await c.plan_resources(action, p, pr, correlation_id.get())

        return plan


class Permission(BasePermission[TModel]):
    def __init__(self, model: Type[TModel], get_model: Callable[[int], TModel] | None = None) -> None:
        super().__init__(model)
        self.get_model = get_model

    async def get_resource(self, pk: int | None = None) -> Resource:
        if not self.get_model:
            return Resource(id='new', kind=self.kind)

        if not pk:
            raise HTTPException(status_code=400, detail='Primary key required')

        data: TModel = await self.get_model(pk)
        return Resource(
            data.id, kind=self.kind, attr={key: getattr(data, key) for key in TModel.__table__.columns.keys()}
        )

    async def __call__(
        self,
        action: str = Depends(get_action),
        p: Principal = Depends(get_principal),
        c: AsyncCerbosClient = Depends(get_cerbos_client),
    ):
        pr = await self.get_resource()

        resp = await c.is_allowed(action, p, pr, correlation_id.get())

        if not resp:
            raise HTTPException(status_code=403, detail='Not Allowed')
