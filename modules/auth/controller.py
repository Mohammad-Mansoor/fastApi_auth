from datetime import datetime, timedelta, UTC
from fastapi import APIRouter, Depends, Request, Response
from sqlalchemy.ext.asyncio import AsyncSession
from core.config import settings
from core.config import settings
from core.database import get_db
from .schemas import LoginResponse, LoginPayload, LogoutResponse, RefreshTokenResponse, RevokeSessionResponse
from .service import AuthService
from .schemas import SingleUserOut


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
        path="/auth/refresh_token"
    )
    return {
            "success": True,
            "message": "Login Successful",
            "access_token": result.get("access_token")
        }


@auth_router.get('/me', response_model=SingleUserOut)
async def me(request:Request, db:AsyncSession = Depends(get_db)):
    result = await auth_service.me(db, request)
    response = {
        "success": True,
        "message": "User Details Fetched Successfully",
        "data": result.get("data"),
        "cached": result.get("cached")
    }
    return response

@auth_router.post("/logout", response_model=LogoutResponse)
async def logout(req:Request, db:AsyncSession = Depends(get_db)):
    result = await auth_service.logout(db, req)
    return {
        "success": True,
        "message": "User Logout Successfully"
    }
    
@auth_router.post('/logout-all', response_model=LogoutResponse)
async def logout_all(req:Request, db:AsyncSession = Depends(get_db)):
    res = await auth_service.logout_all_sessions( db,req)
    return {
        "success":True,
        "message": "All devices Logout Successfully"
    }
@auth_router.post('/logout-other', response_model=LogoutResponse)
async def logout_all_others(req:Request, db:AsyncSession = Depends(get_db)):
    res = await auth_service.logout_all_other_sessions(db, req)
    return {
        "success":True,
        "message": "All Other devices Logout Successfully"
    }
    
@auth_router.post('/refresh_token', response_model=RefreshTokenResponse)
async def refresh_token(req:Request,response:Response, db:AsyncSession = Depends(get_db)):
    res = await auth_service.refresh_token(db, req)
    refresh_token_expiration_date = datetime.now(UTC) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

    response.set_cookie(
        key = "refresh_token",
        value = res.get("refresh_token"),
        expires=refresh_token_expiration_date,
        httponly=True,
        secure= not settings.DEBUG,
        path="/auth/refresh-token"
    )
    return {
        "success": True,
        "message": "Token Refresh Successful",
        "access_token": res.get("access_token")
    }


@auth_router.post("/revoke-session/{sessionId}", response_model=RevokeSessionResponse)
async def revoke_specific_session(req:Request, res:Response, sessionId:str, db:AsyncSession= Depends(get_db)):
    result = await auth_service.revoke_session(req, res, sessionId, db)
    response = {
        "success" : True,
        "message": "Session Revoked Successfully",
        "data": result.session
    }
    return response


@auth_router.post("/not-me")
async def revoke_not_me():
    ...
