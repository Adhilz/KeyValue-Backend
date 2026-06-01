
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from departments.schemas import DepartmentCreate,DepartmentResponse,DepartmentUpdate
from departments.repo import create, get_all_department, get_department_by_id,delete_by_id,update_full,update_partial
from exceptions import BadRequestException, ConflictException, NotFoundException

def _require_non_empty_string(value: str | None, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise BadRequestException(f"{field_name} must be a non-empty string")
    return value.strip()

async def create_department(db:AsyncSession, body: DepartmentCreate):
    name=_require_non_empty_string(body.name,"name")
    result = await create(db,name)
    return result

async def get_all(db:AsyncSession):
    return await get_all_department(db)
        
async def get_by_id(department_id: int, db: AsyncSession):
    department = await get_department_by_id(db, department_id)
    if department is None:
        raise NotFoundException("department not found")
    return department


async def get_department_by_id(department_id: int, db: AsyncSession):
    """Compatibility wrapper so routers calling get_department_by_id continue to work."""
    return await get_by_id(department_id, db)


async def delete_department_by_id(department_id: int, db: AsyncSession):
    deleted_department = await delete_by_id(db, department_id)
    if deleted_department is None:
        raise NotFoundException("Department not found")
    return deleted_department


async def update_full_departments(
    db: AsyncSession,
    department_id: int,
    body: DepartmentUpdate,
):
    name = _require_non_empty_string(body.name, "name")


    try:
        department = await update_full(
            db,
            department_id,
            name,

        )
    except IntegrityError as exc:
        raise ConflictException(f"Some Errors Has Occured") from exc

    if department is None:
        raise NotFoundException("department not found")

    return department


async def update_partial_departments(
    db: AsyncSession,
    department_id: int,
    body: DepartmentUpdate,
):
    data = body.model_dump(exclude_unset=True)

    if "name" in data:
        data["name"] = _require_non_empty_string(data["name"], "name")

    department = await update_partial(
        db, 
        department_id,
        data,
    )

    if department is None:
        raise NotFoundException("department not found")

    return department
