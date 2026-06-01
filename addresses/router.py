from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from addresses import services as address_service
from addresses.schemas import AddressCreateRequest, AddressResponse, AddressUpdate
from auth.dependencies import get_current_user
from auth.schemas import TokenPayload
from database import get_db

router = APIRouter(
    prefix="/addresses",
    tags=["Addresses"],
)


@router.post("", status_code=status.HTTP_201_CREATED, response_model=AddressResponse)
async def create_address(
    body: AddressCreateRequest,
    db: AsyncSession = Depends(get_db),
    _current_user: TokenPayload = Depends(get_current_user),
):
    return await address_service.create_for_employee_request(db, body)


@router.get("", response_model=list[AddressResponse])
async def get_all_addresses(db: AsyncSession = Depends(get_db),
                            _current_user: TokenPayload = Depends(get_current_user),):
    return await address_service.get_all(db)


@router.get("/{address_id}", response_model=AddressResponse)
async def get_address(
    address_id: int,
    db: AsyncSession = Depends(get_db),
    _current_user: TokenPayload = Depends(get_current_user),
):
    return await address_service.get_by_id(db, address_id)


@router.put("/{address_id}", response_model=AddressResponse)
async def update_address(
    address_id: int,
    body: AddressUpdate,
    db: AsyncSession = Depends(get_db),
    _current_user: TokenPayload = Depends(get_current_user),
):
    return await address_service.update(db, address_id, body)


@router.patch("/{address_id}", response_model=AddressResponse)
async def patch_address(
    address_id: int,
    body: AddressUpdate,
    db: AsyncSession = Depends(get_db),
    _current_user: TokenPayload = Depends(get_current_user),
):
    return await address_service.update(db, address_id, body)


@router.delete("/{address_id}")
async def delete_address(
    address_id: int,
    db: AsyncSession = Depends(get_db),
    _current_user: TokenPayload = Depends(get_current_user),
):
    return await address_service.delete_by_id(db, address_id)