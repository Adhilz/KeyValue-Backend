from sqlalchemy.ext.asyncio import AsyncSession

from addresses.repo import (
    create as create_address_repo,
    delete as delete_address_repo,
    get_all as get_all_addresses_repo,
    get_by_id as get_address_repo,
    update as update_address_repo,
)
from addresses.schemas import AddressCreate, AddressCreateRequest, AddressUpdate
from employees.repo import get_by_id as get_employee_repo
from exceptions import BadRequestException, NotFoundException


def _validate_postal_code_for_country(country: str, postal_code: str) -> None:
    if not postal_code.isdigit():
        raise BadRequestException("Postal code must contain only digits [0-9]")

    normalized_country = country.strip().upper()
    postal_code_length = len(postal_code)

    if normalized_country in ("US", "USA") and postal_code_length != 5:
        raise BadRequestException("US ZIP codes must be exactly 5 digits")

    if normalized_country in ("IN", "INDIA") and postal_code_length != 6:
        raise BadRequestException("Indian PIN codes must be exactly 6 digits")

async def create(
    db: AsyncSession,
    employee_id: int,
    address: AddressCreate,
):
    employee = await get_employee_repo(db, employee_id)

    if employee is None:
        raise NotFoundException("Employee not found")

    return await create_address_repo(
        db,
        employee_id,
        address,
    )


async def create_for_employee_request(
    db: AsyncSession,
    body: AddressCreateRequest,
):
    return await create(db, body.employee_id, body)


async def get_all(db: AsyncSession):
    return await get_all_addresses_repo(db)


async def get_by_id(db: AsyncSession, address_id: int):
    address = await get_address_repo(db, address_id)

    if address is None:
        raise NotFoundException("Address not found")

    return address


async def update(
    db: AsyncSession,
    address_id: int,
    body: AddressUpdate,
):
    data = body.model_dump(exclude_unset=True)

    if not data:
        raise BadRequestException("At least one address field must be provided")

    current_address = await get_address_repo(db, address_id)

    if current_address is None:
        raise NotFoundException("Address not found")

    merged_country = data.get("country", current_address.country)
    merged_postal_code = data.get("postal_code", current_address.postal_code)

    _validate_postal_code_for_country(merged_country, merged_postal_code)

    address = await update_address_repo(db, address_id, body)

    if address is None:
        raise NotFoundException("Address not found")

    return address


async def delete_by_id(db: AsyncSession, address_id: int):
    deleted = await delete_address_repo(db, address_id)

    if not deleted:
        raise NotFoundException("Address not found")

    return {"message": "Address deleted successfully"}
