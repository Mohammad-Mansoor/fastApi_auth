from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from .schemas import LoginResponse, LoginPayload
from .service import AuthService


auth_router = APIRouter()
auth_service = AuthService()

@auth_router.post("/login", response_model = LoginResponse)
async def login(data: LoginPayload, db:AsyncSession = Depends(get_db)):
    print("login payload", data)
    return await auth_service.login(db, data)

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
