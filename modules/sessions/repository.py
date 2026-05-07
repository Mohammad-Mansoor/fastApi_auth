from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from .models import Session
from .schema import CreateSession


class SessionRepository:
    async def create_session(self, db:AsyncSession, data:CreateSession):
        session_data = Session(**data.model_dump())
        db.add(session_data)
        return session_data
        
    async def get_session_by_id(self, db:AsyncSession, sessionId: str):
        result = await db.execute(select(Session).where(Session.id == sessionId))
        return result.scalars().first()
        ...
    async def get_sessions_by_user_id(self, db:AsyncSession, userId: str):
        
        ...
    async def get_all_sessions(self, db:AsyncSession, query: dict):
        ...
    async def revoke_session(self, db:AsyncSession, sessionId: str):
        ...
    async def revoke_user_sessions(self, db:AsyncSession, userId: str):
        ...
    ...