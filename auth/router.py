from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from auth import service as auth_service
from auth.schemas import TokenResponse
from database.connection import get_db
from fastapi.security import OAuth2PasswordRequestForm
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=TokenResponse)
async def login(
    form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    token = await auth_service.login(db, form.username, form.password)
    logger.info(f"User {form.username} logged in successfully")
    return TokenResponse(access_token=token)
