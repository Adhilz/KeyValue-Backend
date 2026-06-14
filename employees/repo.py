from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from models.address import Address
from models.employee import Employee


def _employee_stmt(employee_id: int):
    return (
        select(Employee)
        .options(selectinload(Employee.addresses), selectinload(Employee.departments))
        .where(
            Employee.id == employee_id,
            Employee.deleted_at.is_(None),
        )
    )


async def create(
    db: AsyncSession,
    name: str,
    email: str,
    password: str,
    role: str,
    status: str,
    age: int | None = None,
) -> Employee:
    db_employee = Employee(
        name=name,
        email=email,
        age=age,
        password_hash=password,
        role=role,
        status=status,
    )
    db.add(db_employee)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise
    await db.refresh(db_employee)
    return db_employee


async def get_all_employees(db: AsyncSession):
    stmt = (
        select(Employee)
        .options(selectinload(Employee.addresses), selectinload(Employee.departments))
        .where(Employee.deleted_at.is_(None))
    )
    result = await db.scalars(stmt)
    return result.all()


async def get_by_id(db: AsyncSession, employee_id: int):
    stmt = _employee_stmt(employee_id)
    result = await db.scalar(stmt)
    return result


async def delete_by_id(db: AsyncSession, employee_id: int):
    result = await db.scalar(_employee_stmt(employee_id))
    if result is None:
        return None
    await db.delete(result)
    await db.commit()
    return {"message": f"Employee with id {employee_id} deleted successfully"}


async def update_full(db: AsyncSession, employee_id: int, body: dict) -> Employee:
    result = await db.scalar(_employee_stmt(employee_id))
    if result is None:
        return None

    result.name = body["name"]
    result.email = body["email"]
    result.age = body["age"]
    result.status = body["status"]
    result.role = body["role"]

    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise

    await db.refresh(result)
    return result


async def update_partial(db: AsyncSession, employee_id: int, data: dict) -> Employee:
    result = await db.scalar(_employee_stmt(employee_id))
    if result is None:
        return None

    if "name" in data:
        result.name = data["name"].strip()

    if "email" in data:
        result.email = data["email"].strip()

    if "age" in data:
        result.age = data["age"]

    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise

    await db.refresh(result)
    return result


async def get_by_email(db: AsyncSession, email: str):
    stmt = select(Employee).where(
        Employee.email == email,
        Employee.deleted_at.is_(None),
    )
    result = await db.scalars(stmt)
    return result.first()


async def delete_address(
    db: AsyncSession,
    employee_id: int,
    address_id: int,
):
    stmt = select(Address).where(
        Address.id == address_id,
        Address.employee_id == employee_id,
    )

    address = await db.scalar(stmt)

    if address is None:
        return False

    await db.delete(address)
    await db.commit()

    return True
