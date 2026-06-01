from sqlalchemy.ext.asyncio import AsyncSession

from auth.utils import (
    create_access_token,
    refresh_access_token,
    verify_password,
    create_refresh_token,
)

from employees import repo
from exceptions import UnauthorizedException


async def login(db: AsyncSession, email: str, password: str) -> str:

    employee = await repo.get_by_email(db, email)

    if employee is None:
        raise UnauthorizedException("Invalid Email or password")
    if not verify_password(password, employee.password_hash):
        raise UnauthorizedException("Invalid Email or  Password")
    access_token = create_access_token(
        {"id": employee.id, "email": employee.email, "role": employee.role}
    )
    refresh_token = create_refresh_token(
        {"id": employee.id, "email": employee.email, "role": employee.role}
    )
    return access_token, refresh_token


async def refresh(refresh_token: str) -> str:
    token = refresh_access_token(refresh_token)

    if token is None:
        raise UnauthorizedException("Invalid refresh token")

    return token
