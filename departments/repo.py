from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from models.department import Department


def department_stmt(department_id: int):
    return select(Department).where(
        Department.id == department_id,
        Department.deleted_at.is_(None),
    )


async def create(db: AsyncSession, name: str) -> Department:
    db_department = Department(name=name)
    db.add(db_department)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise
    await db.refresh(db_department)
    return db_department


async def get_all_department(db: AsyncSession):
    stmt = select(Department).where(Department.deleted_at.is_(None))
    result = await db.scalars(stmt)
    return result.all()


async def get_department_id(db: AsyncSession, department_id: int):
    stmt = department_stmt(department_id)
    result = await db.scalar(stmt)
    return result


async def delete_by_id(db: AsyncSession, department_id: int):
    stmt = department_stmt(department_id)
    result = await db.scalar(stmt)
    if result is None:
        return None
    await db.delete(result)
    await db.commit()
    return {"message": f"Department with {department_id} deleted Successfully"}


async def update_full(db: AsyncSession, department_id: int, name: str) -> Department:
    result = await db.scalar(department_stmt(department_id))
    if result is None:
        return None
    result.name = name
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise
    await db.refresh(result)
    return result


async def update_partial(
    db: AsyncSession, department_id: int, data: dict
) -> Department:
    result = await db.scalar(department_stmt(department_id))
    if result is None:
        return None
    if "name" in data:
        result.name = data["name"].strip()
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise
    await db.refresh(result)
    return result
