from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from auth.schemas import TokenPayload
from auth.utils import decode_access_token
from exceptions import NotFoundException, UnauthorizedException
from models.employee import EmployeeRole

oauth2_scheme= OAuth2PasswordBearer(tokenUrl="/auth/login")
def get_current_user(token: str= Depends(oauth2_scheme))->TokenPayload:
    payload=decode_access_token(token)
    if payload is None:
        raise UnauthorizedException("Invalid or expired token")
    return payload
def role_checker(*roles: EmployeeRole):
    def role_checker(
            current_user: TokenPayload = Depends(get_current_user),
    )->TokenPayload:
        if current_user.get("role") not in roles:
            raise NotFoundException(
                "You Do not Have Permission to perform this action"
            )
        return current_user
    return role_checker
    