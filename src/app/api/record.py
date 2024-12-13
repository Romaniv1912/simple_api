from typing import TYPE_CHECKING

from fastapi import APIRouter
from fastapi.params import Depends

from cerbos.sdk.model import PlanResourcesResponse
from src.app.model import Record
from src.app.schema.record import GetRecordListDetails
from src.app.service.record import record_service
from src.common.pagination import DependsPagination, Page, paging_data
from src.common.permission import Permission, PlanPermission
from src.database import CurrentSession

if TYPE_CHECKING:
    from sqlalchemy import Select

router = APIRouter()


@router.get(
    '',
    summary='Get records',
    description='Get all records by pagination',
    dependencies=[DependsPagination],
    response_model=Page[GetRecordListDetails],
)
async def get_pagination_record(
    db: CurrentSession, plan: PlanResourcesResponse = Depends(PlanPermission(Record))
) -> Page[GetRecordListDetails]:
    select: Select = record_service.get_select(plan)
    return await paging_data(db, select, GetRecordListDetails)


@router.post(
    '',
    summary='Create new record',
    description='Create new record and send telegram message',
    status_code=201,
    dependencies=[Depends(Permission(Record))],
)
def create_record(
    data: GetRecordListDetails = Depends(record_service.create),
) -> GetRecordListDetails:
    return data
