from typing import Any, Awaitable, Callable, Dict, List, Type, TypeVar

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
    """Get principal from current user"""
    attr = {'id': user.id}

    if user.users:
        attr['users'] = {user.id for user in user.users}

    return Principal(id=str(user.username), roles={role.name.lower() for role in user.roles}, attr=attr)


async def get_cerbos_client() -> AsyncCerbosClient:
    async with AsyncCerbosClient(settings.CERBOS.http_url) as client:
        yield client


def get_action(act: str | None = None):
    def func(request: Request) -> str:
        if act:
            return act

        action = ACTIONS_DICT.get(request.method)

        if action is None:
            raise HTTPException(403, 'Method Not Allowed')

        return action

    return func


async def get_plan(
    action: str, principal: Principal, resource: ResourceDesc, client: AsyncCerbosClient, cid: str | None = None
) -> PlanResourcesResponse:
    """Return plan from Cerbos"""
    plan: PlanResourcesResponse = await client.plan_resources(action, principal, resource, cid)

    return plan


async def raise_not_allowed(
    action: str, principal: Principal, resource: Resource, client: AsyncCerbosClient, cid: str | None = None
) -> None:
    """Raise exception if action is not allowed"""
    resp = await client.is_allowed(action, principal, resource, cid)

    if not resp:
        raise HTTPException(status_code=403, detail='Not Allowed')


async def get_resource(kind: str, data: TModel, mapper: Callable[[TModel], Dict] | List[str] | None = None) -> Resource:
    """
    Get resource for Cerbos allow request

    :param kind: kind of resource
    :param data: Instance of model
    :param mapper: Custom mapper for model
    :return:
    """
    if not data:
        return Resource(id='new', kind=kind)

    if isinstance(mapper, Callable):
        attr = mapper(data)
    elif isinstance(mapper, List):
        attr = {key: getattr(data, key) for key in mapper}
    else:
        attr = {key: getattr(data, key) for key in data.__table__.columns.keys()}

    return Resource(str(data.id), kind=kind, attr=attr)


def Permission(
    model: Type[TModel],
    *,
    action: str | None = None,
    getter: Callable[[Any, ...], Awaitable[TModel]] | None = None,
    mapper: Callable[[TModel], Dict] | List[str] | None = None,
    with_plan: bool = False,
) -> Callable:
    """
    Set permission guard for route

    :param model: model to get access for
    :param action: action, set default by <fastapi.Request.method>
    :param getter: get model function, for creating resource
    :param mapper: map model function, default get all columns
    :param with_plan: whether to get plan
    """
    kind = model.__name__.lower()
    model_getter = getter or (lambda: None)

    async def call(
        act: str = Depends(get_action(action)),
        data: TModel = Depends(model_getter),
        principal: Principal = Depends(get_principal),
        client: AsyncCerbosClient = Depends(get_cerbos_client),
    ) -> PlanResourcesResponse | TModel | None:
        cid = correlation_id.get()

        if with_plan:
            return await get_plan(act, principal, ResourceDesc(kind), client, cid)

        resource = await get_resource(kind, data, mapper)
        await raise_not_allowed(act, principal, resource, client, cid)

        return data

    return call
