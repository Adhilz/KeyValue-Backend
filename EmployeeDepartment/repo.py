from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from models.employee_department import EmployeeDepartment
from sqlalchemy.ext.asyncio import AsyncSession


async def attach(db: AsyncSession, emp_id: int, dept_id: int) -> EmployeeDepartment:
    stmt = EmployeeDepartment(emp_id=emp_id, dept_id=dept_id)
    db.add(stmt)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise
    await db.refresh(stmt)
    return stmt


async def detach(
    db: AsyncSession,
    employee_id: int,
    department_id: int,
):
    stmt = select(EmployeeDepartment).where(
        EmployeeDepartment.emp_id == employee_id,
        EmployeeDepartment.dept_id == department_id,
    )

    result = await db.scalar(stmt)

    if result is None:
        return None

    await db.delete(result)
    await db.commit()

    return result


# async def get_by_id(
#         db:AsyncSession,
#         body
# )->Employee
