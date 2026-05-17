from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from .models import Session
from .schema import CreateSession
from common.query_builder.query_builder import SQLAlchemyQueryHelper,QueryConfig

class SessionRepository:
    async def create_session(self, db:AsyncSession, data:CreateSession):
        session_data = Session(**data.model_dump())
        db.add(session_data)
        return session_data
        
    async def get_session_by_id(self, db:AsyncSession, sessionId: str):
        result = await db.execute(select(Session).where(Session.id == sessionId))
        return result.scalars().first()
        ...
    async def get_sessions_by_user_id(self, db:AsyncSession, userId: str, query: dict, queryConfig):
        query = SQLAlchemyQueryHelper.for_(
            model= Session,
            session = db,
            options = query,
            config = queryConfig
        )
        result = await query.get_many_and_meta()
        return result
        
        
        ...
    async def get_all_sessions(self, db:AsyncSession, query: dict, queryConfig):
        query = SQLAlchemyQueryHelper.for_(
            model = Session,
            session = db,
            options = query,
            config = queryConfig
        )
        result  = await query.get_many_and_meta()
        return result
    
    async def get_all_active_session_of_user(self, db:AsyncSession, userId:str):
        result = await db.execute(select(Session).where(Session.userId == userId, Session.isValid == True))
        user_sessions = result.sacalrs().all()
        return user_sessions
        ...
    async def revoke_session(self, db:AsyncSession, sessionId: str, revokeReason:str):
        
        ...
    async def revoke_user_sessions(self, db:AsyncSession, userId: str):
        ...
    ...