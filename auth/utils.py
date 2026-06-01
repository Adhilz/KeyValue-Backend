from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from config import setting

import bcrypt


def hash_password(plain: str) -> str:
    return bcrypt.hashpw(plain.encode(), bcrypt.gensalt()).decode()


def verify_password(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(plain.encode(), hashed.encode())


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=setting.jwt_expiry_minutes)
    to_encode["exp"] = expire
    return jwt.encode(to_encode, setting.jwt_Secret, algorithm=setting.jwt_algorithm)


def create_refresh_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=setting.jwt_refresh_expiry_minutes
    )
    to_encode["exp"] = expire
    to_encode["type"] = "refresh"

    return jwt.encode(to_encode, setting.jwt_Secret, algorithm=setting.jwt_algorithm)


def decode_access_token(token: str) -> dict | None:
    try:
        return jwt.decode(token, setting.jwt_Secret, algorithms=[setting.jwt_algorithm])
    except JWTError:
        return None


def refresh_access_token(refresh_token: str) -> str | None:
    try:
        payload = jwt.decode(
            refresh_token,
            setting.jwt_Secret,
            algorithms=[setting.jwt_algorithm],
        )

        if payload.get("type") != "refresh":
            return None

        return create_access_token(
            {"id": payload.get("id"), "email": payload.get("email")}
        )

    except JWTError:
        return None
