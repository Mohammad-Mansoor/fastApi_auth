from datetime import UTC, datetime
from modules.users.models import User
from modules.sessions.models import Session
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession


class AuthRepository:
    
    async def get_active_sessions_by_user_id(self,userId:str, db:AsyncSession):
        stmt = select(Session).where(Session.userId == userId, Session.isValid.is_(True))
        res = await db.execute(stmt)
        result = res.scalars().all()
        return result
    
    async def get_session_by_refresh_token(self, refresh, db:AsyncSession):
        stmt = select(Session).where(Session.refreshToken == refresh)
        res = await db.execute(stmt)
        result = res.scalar_one_or_none()
        return result
    
    async def logout_all_active_sessions_by_user_id(self,userId:str, db:AsyncSession):
        now = datetime.now(UTC)
        stmt = (
            update(Session)
            .where(Session.userId == userId, Session.isValid.is_(True))
            .values(isValid=False, logoutAt=now)
            .returning(Session.id)
            # we can return specific fields base on the need like returning id useful for websocket disconnects, cache invalidation etc
        )
        result = await db.execute(stmt)
        return result
    
    async def logout_other_sessions_except_current_by_user_id(self,userId: str, currentSessionId:str, db:AsyncSession):
        now = datetime.now(UTC)
        stmt = (
            update(Session)
            .where(Session.userId == userId, Session.id != currentSessionId, Session.isValid.is_(True))
            .values(isValid = False, logoutAt=now)
            .returning(Session.id)
        )
        result = await db.execute(stmt)
        return result

        