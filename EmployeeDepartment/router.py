from fastapi import Depends, status
from fastapi import APIRouter

from EmployeeDepartment.schema import EmployeeDepartmentCreate
from EmployeeDepartment import services
from sqlalchemy.ext.asyncio import AsyncSession

from auth.dependencies import get_current_user
from auth.schemas import TokenPayload
from database.connection import get_db

router = APIRouter(
    prefix="/employee-departments",
    tags=["Employee - Department"],
)


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_department(
    body: EmployeeDepartmentCreate,
    db: AsyncSession = Depends(get_db),
    _current_user: TokenPayload = Depends(get_current_user),
):
    return await services.create(db, body)
