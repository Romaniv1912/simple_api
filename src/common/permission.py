from typing import Awaitable, Callable, Dict, Generic, List, Type, TypeVar

from asgi_correlation_id import correlation_id
from fastapi import HTTPException, Request
from fastapi.params import Depends

from cerbos.sdk.client import AsyncCerbosClient
from cerbos.sdk.model import PlanResourcesResponse, Principal, Resource, ResourceDesc
from src.app.model import User
from src.core.conf import settings
from src.utils.user import get_current_user

TModel = TypeVar('TModel')
ACTIONS_DICT = {'GET': 'read', 'POST': 'create', 'PUST': 'update', 'PATCH': 'update', 'DELETE': 'delete'}


def get_principal(user: User = Depends(get_current_user)) -> Principal:
    attr = {'id': user.id}

    if user.users:
        attr['users'] = {user.id for user in user.users}

    return Principal(id=str(user.username), roles={role.name.lower() for role in user.roles}, attr=attr)


async def get_cerbos_client() -> AsyncCerbosClient:
    async with AsyncCerbosClient(settings.CERBOS.http_url) as client:
        yield client


class Permission(Generic[TModel]):
    def __init__(
        self,
        model: Type[TModel],
        *,
        action: str | None = None,
        getter: Callable[[int], Awaitable[TModel]] | None = None,
        mapper: Callable[[TModel], Dict] | List[str] | None = None,
        with_plan: bool = False,
        pk: str = 'pk',
    ) -> None:
        self.model = model
        self.action = action
        self.with_plan = with_plan
        self.getter = getter
        self.mapper = mapper
        self.data = None
        self.pk = pk

    @property
    def kind(self):
        return self.model.__name__.lower()

    def get_action(self, request: Request) -> str:
        if self.action is not None:
            return self.action

        action = ACTIONS_DICT.get(request.method)

        if action is None:
            raise HTTPException(403, 'Method Not Allowed')

        return action

    async def get_resource(self, pk: int | None = None) -> Resource:
        if not self.getter:
            return Resource(id='new', kind=self.kind)

        if not pk:
            raise HTTPException(status_code=400, detail='Primary key is required')

        self.data: TModel = await self.getter(pk)

        if isinstance(self.mapper, Callable):
            attr = self.mapper(self.data)
        elif isinstance(self.mapper, List):
            attr = {key: getattr(self.data, key) for key in self.mapper}
        else:
            attr = {key: getattr(self.data, key) for key in self.model.__table__.columns.keys()}

        return Resource(str(self.data.id), kind=self.kind, attr=attr)

    async def __call__(
        self,
        request: Request,
        p: Principal = Depends(get_principal),
        c: AsyncCerbosClient = Depends(get_cerbos_client),
    ) -> PlanResourcesResponse | TModel | None:
        action = self.get_action(request)
        cid = correlation_id.get()

        if not self.with_plan:
            pk = request.path_params.get(self.pk)
            pr = await self.get_resource(int(pk) if pk else None)
            resp = await c.is_allowed(action, p, pr, cid)

            if not resp:
                raise HTTPException(status_code=403, detail='Not Allowed')

            return self.data

        pr = ResourceDesc(self.kind)

        plan: PlanResourcesResponse = await c.plan_resources(self.get_action(request), p, pr, cid)

        return plan
