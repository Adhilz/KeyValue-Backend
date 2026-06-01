from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from auth.utils import hash_password
from employees.repo import (
    create as create_employee_repo,
    delete_by_id as delete_employee_repo,
    get_all_employees,
    get_by_id as get_employee_repo,
    update_full as update_full_repo,
    update_partial as update_partial_repo,
    delete_address 
)
from addresses.schemas import AddressCreate
from employees.schemas import EmployeeCreate, EmployeeFullUpdate, EmployeeUpdate
from exceptions import BadRequestException, ConflictException, NotFoundException
from addresses import repo as address_repo

def _require_non_empty_string(value: str | None, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise BadRequestException(f"{field_name} must be a non-empty string")
    return value.strip()


async def create(db: AsyncSession, body: EmployeeCreate):
    hashed_password = hash_password(body.password)

    name = _require_non_empty_string(body.name, "name")
    email = _require_non_empty_string(str(body.email), "email")

    try:
        employee = await create_employee_repo(
            db,
            name,
            email,
            password=hashed_password,
            age=body.age,
        )

        if body.address:
            await address_repo.create(
                db=db,
                employee_id=employee.id,
                address=body.address,
            )

        return await get_employee_repo(db, employee.id)

    except IntegrityError as exc:
        raise ConflictException(
            f"Email '{email}' is already in use"
        ) from exc


async def get_all(db: AsyncSession):
    return await get_all_employees(db)


async def get_by_id(employee_id: int, db: AsyncSession):
    employee = await get_employee_repo(db, employee_id)
    if employee is None:
        raise NotFoundException("Employee not found")
    return employee


async def delete_by_id(employee_id: int, db: AsyncSession):
    deleted_employee = await delete_employee_repo(db, employee_id)
    if deleted_employee is None:
        raise NotFoundException("Employee not found")
    return deleted_employee


async def update_full(
    db: AsyncSession,
    employee_id: int,
    body: EmployeeFullUpdate,
):
    name = _require_non_empty_string(body.name, "name")
    email = _require_non_empty_string(str(body.email), "email")

    try:
        employee = await update_full_repo(
            db,
            employee_id,
            name,
            email,
            body.age,
        )
    except IntegrityError as exc:
        raise ConflictException(f"Email '{email}' is already in use") from exc

    if employee is None:
        raise NotFoundException("Employee not found")

    return employee


async def update_partial(
    db: AsyncSession,
    employee_id: int,
    body: EmployeeUpdate,
):
    data = body.model_dump(exclude_unset=True)

    if "name" in data:
        data["name"] = _require_non_empty_string(data["name"], "name")

    if "email" in data:
        data["email"] = _require_non_empty_string(str(data["email"]), "email")

    employee = await update_partial_repo(
        db,
        employee_id,
        data,
    )

    if employee is None:
        raise NotFoundException("Employee not found")

    return employee

async def delete_employee_address(
    db: AsyncSession,
    employee_id: int,
    address_id: int,
):
    deleted = await delete_address(
        db,
        employee_id,
        address_id,
    )

    if not deleted:
        raise NotFoundException(
            
            "Address not found for employee",
        )

    return {
        "message": "Address deleted successfully"
    }