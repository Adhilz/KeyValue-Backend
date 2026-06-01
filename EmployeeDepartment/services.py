
from EmployeeDepartment.schema import EmployeeDepartmentCreate
from exceptions import BadRequestException, NotFoundException
from sqlalchemy.ext.asyncio import AsyncSession
from EmployeeDepartment.repo import attach,detach as detach_repo
from employees import repo as employee_repo
from departments import repo as department_repo
def _require_non_empty_string(value: str | None, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise BadRequestException(f"{field_name} must be a non-empty string")
    return value.strip()


async def create(db: AsyncSession, body: EmployeeDepartmentCreate):
    
    employee= await employee_repo.get_by_id(
        db,
        body.emp_id
    )
    department = await department_repo.get_department_by_id(
        db,
        body.dept_id
    )
    if employee is None:
        raise  NotFoundException(f"Employee not found ")
    if department is None:
        raise NotFoundException(f"Department  not found ")

    return await attach(
        db,
        body.emp_id,
        body.dept_id
        )
async def detach(
    db: AsyncSession,
    employee_id: int,
    department_id: int,
):
    mapping = await detach_repo(
        db,
        employee_id,
        department_id,
    )

    if mapping is None:
        raise NotFoundException(
            
           "Employee department mapping not found",
        )

    return {"message": "Department detached successfully"}

