from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from addresses.schemas import AddressCreate, AddressUpdate
from models.address import Address


async def create(
    db: AsyncSession,
    employee_id: int,
    address: AddressCreate,
):
    address_obj = Address(
        employee_id=employee_id,
        line=address.line,
        city=address.city,
        postal_code=address.postal_code,
        country=address.country,
    )

    db.add(address_obj)

    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise

    await db.refresh(address_obj)

    return address_obj


async def get_all(db: AsyncSession):
    result = await db.scalars(select(Address).order_by(Address.id))
    return result.all()


async def get_by_id(db: AsyncSession, address_id: int):
    stmt = select(Address).where(Address.id == address_id)
    return await db.scalar(stmt)


async def get_by_employee_id(db: AsyncSession, employee_id: int):
    stmt = (
        select(Address).where(Address.employee_id == employee_id).order_by(Address.id)
    )
    result = await db.scalars(stmt)
    return result.all()


async def get_by_employee_and_id(db: AsyncSession, employee_id: int, address_id: int):
    stmt = select(Address).where(
        Address.employee_id == employee_id,
        Address.id == address_id,
    )
    return await db.scalar(stmt)


async def update(
    db: AsyncSession,
    address_id: int,
    data: AddressUpdate,
):
    address = await db.scalar(select(Address).where(Address.id == address_id))

    if address is None:
        return None

    update_data = data.model_dump(exclude_unset=True)

    if "line" in update_data:
        address.line = update_data["line"]

    if "city" in update_data:
        address.city = update_data["city"]

    if "postal_code" in update_data:
        address.postal_code = update_data["postal_code"]

    if "country" in update_data:
        address.country = update_data["country"]

    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise

    await db.refresh(address)
    return address


async def delete(db: AsyncSession, address_id: int):
    address = await db.scalar(select(Address).where(Address.id == address_id))

    if address is None:
        return False

    await db.delete(address)
    await db.commit()
    return True
