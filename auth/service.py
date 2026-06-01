from sqlalchemy.ext.asyncio import AsyncSession

from auth.utils import create_access_token, verify_password
from employees import repo
from exceptions import UnauthorizedException


async def login(db: AsyncSession, email: str, password: str) -> str:

    employee = await repo.get_by_email(db, email)

    if employee is None:
        raise UnauthorizedException("Invalid Email or password")
    if not verify_password(password, employee.password_hash):
        raise UnauthorizedException("Invalid Email or  Password")
    return create_access_token(
        {"id": employee.id, "email": employee.email, "role": employee.role.value}
    )
