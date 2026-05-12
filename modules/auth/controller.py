from datetime import datetime, timedelta, UTC
from fastapi import APIRouter, Depends, Request, Response
from sqlalchemy.ext.asyncio import AsyncSession
from core.config import settings
from core.config import settings
from core.database import get_db
from .schemas import LoginResponse, LoginPayload
from .service import AuthService


auth_router = APIRouter(prefix = "/auth", tags=["Auth"])
auth_service = AuthService()

@auth_router.post("/login", response_model = LoginResponse)
async def login(data: LoginPayload,request: Request, response:Response, db:AsyncSession = Depends(get_db) ):
    print("login payload", data)
    result = await auth_service.login(db, data, request)
    device_id_expiration_date = datetime.now(UTC) + timedelta(days=365)
    refresh_token_expiration_date = datetime.now(UTC) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    response.set_cookie(
        key = "device_id",
        value = result.get("device_id"),
        expires=device_id_expiration_date,
        secure = not settings.DEBUG,
        httponly=True
    )
    response.set_cookie(
        key = "refresh_token",
        value = result.get("refresh_token"),
        expires=refresh_token_expiration_date,
        httponly=True,
        secure= not settings.DEBUG,
        path="/auth/refresh-token"
    )
    return {
            "success": True,
            "message": "Login Successful",
            "access_token": result.get("access_token")
        }


@auth_router.get('/me')
async def me(request:Request, db:AsyncSession = Depends(get_db)):
    return await auth_service.me(db, request)

@auth_router.post("/logout")
async def logout():
    ...


@auth_router.post("/logout-all")
async def logout_all():
    ...


@auth_router.post("/logout-other-sessions")
async def logout_other_sessions():
    ...

@auth_router.post("/revoke-session")
async def revoke_specific_session():
    ...

@auth_router.post("/not-me")
async def revoke_not_me():
    ...
