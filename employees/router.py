from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from auth.dependencies import get_current_user, role_checker
from auth.schemas import TokenPayload
from database import get_db
from employees import services as employee_service
from employees.schemas import EmployeeCreate, EmployeeFullUpdate, EmployeeResponse, EmployeeUpdate, EmployeeidResponse
from EmployeeDepartment.schema import EmployeeDepartmentCreate
from EmployeeDepartment import services
from models.employee import EmployeeRole
router = APIRouter(
    prefix="/employee",
    tags=["Employees"],
)


@router.post("", status_code=status.HTTP_201_CREATED, response_model=EmployeeResponse,dependencies=[Depends(role_checker(EmployeeRole.HR))])
async def create_employee(
    body: EmployeeCreate,
    db: AsyncSession = Depends(get_db),
    _current_user: TokenPayload = Depends(get_current_user),
):
    return await employee_service.create(
        db,
        body
    )


# @router.get("",response_model=list[EmployeeResponse])
# async def get_all_employees(
#     db: AsyncSession = Depends(get_db),
# ):
#     return await employee_service.get_all(db)


@router.get("/{employee_id}",response_model=EmployeeidResponse)
async def get_employee(
    employee_id: int,
    db: AsyncSession = Depends(get_db),
    _current_user: TokenPayload = Depends(get_current_user),
):
    return await employee_service.get_by_id(
        employee_id,
        db,
    )


@router.put("/{employee_id}",dependencies=[Depends(role_checker(EmployeeRole.HR))])
async def update_employee(
    employee_id: int,
    body: EmployeeFullUpdate,
    db: AsyncSession = Depends(get_db),
    _current_user: TokenPayload = Depends(get_current_user),
):
    return await employee_service.update_full(
        db,
        employee_id,
        body,
    )


@router.patch("/{employee_id}")
async def patch_employee(
    employee_id: int,
    body: EmployeeUpdate,
    db: AsyncSession = Depends(get_db),
    _current_user: TokenPayload = Depends(get_current_user),
):
    return await employee_service.update_partial(
        db,
        employee_id,
        body,
    )


@router.delete("/{employee_id}",dependencies=[Depends(role_checker(EmployeeRole.HR))])
async def delete_employee(
    employee_id: int,
    db: AsyncSession = Depends(get_db),
    _current_user: TokenPayload = Depends(get_current_user),
):
    return await employee_service.delete_by_id(
        employee_id,
        db,
    )

    
@router.get("",response_model=list[EmployeeResponse])
async def get_all_employees(
    db: AsyncSession = Depends(get_db),
    _current_user: TokenPayload = Depends(get_current_user),
):
    return await employee_service.get_all(db)



@router.post("/{employee_id}/departments/{department_id}", status_code=status.HTTP_201_CREATED)
async def attach_department(
    employee_id: int,
    department_id: int,
    db: AsyncSession = Depends(get_db),
    _current_user: TokenPayload = Depends(get_current_user),
):
    body = EmployeeDepartmentCreate(emp_id=employee_id, dept_id=department_id)
    return await services.create(db, body)
@router.delete("/{employee_id}/departments/{department_id}")
async def detach_department(
    employee_id: int,
    department_id: int,
    db: AsyncSession = Depends(get_db),
    _current_user: TokenPayload = Depends(get_current_user),
):
    return await services.detach(db, employee_id, department_id)
    
@router.delete("/{employee_id}/addresses/{address_id}")
async def delete_address(
    employee_id: int,
    address_id: int,
    db: AsyncSession = Depends(get_db),
    _current_user: TokenPayload = Depends(get_current_user),
):
    return await employee_service.delete_employee_address(db, employee_id, address_id)