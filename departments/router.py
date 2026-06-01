from fastapi import status
from fastapi import APIRouter, Depends

from auth.schemas import TokenPayload
from database.connection import get_db
from departments.schemas import DepartmentCreate, DepartmentResponse, DepartmentUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from departments import services


router = APIRouter(
    prefix="/department",
    tags=["Department"],
)


@router.post("", status_code=status.HTTP_201_CREATED, response_model=DepartmentResponse)
async def create_department(
    body: DepartmentCreate,
    db: AsyncSession = Depends(get_db),
):
    return await services.create_department(
        db,
        body
    )


@router.get("",response_model=list[DepartmentResponse])
async def get_all_departments(
    db: AsyncSession = Depends(get_db),
):
    return await services.get_all(db)


@router.get("/{department_id}",response_model=DepartmentResponse)
async def get_department(
    department_id: int,
    db: AsyncSession = Depends(get_db),
):
    return await services.get_department_by_id(
        department_id,
        db,
    )


@router.put("/{department_id}")
async def update_department(
    department_id: int,
    body: DepartmentUpdate,
    db: AsyncSession = Depends(get_db),
):
    return await services.update_full_departments(
        db,
        department_id,
        body,
    )


@router.patch("/{department_id}")
async def patch_department(
    department_id: int,
    body: DepartmentUpdate,
    db: AsyncSession = Depends(get_db),
):
    return await services.update_partial_departments(
        db,
        department_id,
        body,
    )


@router.delete("/{department_id}")
async def delete_department(
    department_id: int,
    db: AsyncSession = Depends(get_db),
):
    return await services.delete_department_by_id(
        department_id,
        db,
    )
