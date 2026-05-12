from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from core.schemas import QueryOptionsDto
from .service import SessionService



session_route = APIRouter()
session_service = SessionService()


@session_route.get("/sessions")
async def get_all_sessions(request: Request, query: QueryOptionsDto = Depends() ,db: AsyncSession = Depends(get_db), ):
    result = await session_service.get_all_sessions(db, request, query)
    return result
    ...
@session_route.get("/sessions/{sessionId}")
async def get_single_sessions():
    ...
@session_route.get("/sessions/user/{userId}")
async def get_userbase_sessions():
    ...
