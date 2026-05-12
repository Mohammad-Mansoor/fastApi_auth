from fastapi import Depends, Request
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from common.query_builder.query_builder import QueryConfig
from core.exceptions.app_exception import AppException
from core.schemas import QueryOptionsDto
from .repository import SessionRepository
from infrastructure.redis.service import RedisCacheService
from infrastructure.redis.keys import SessionCacheKeys
from .models import Session


class SessionService:
    def __init__(self):
        self.sessionRepo = SessionRepository()
        self.redis_cache_service = RedisCacheService()
        
        
    async def get_session_by_id(self, db: AsyncSession,sessionId: str):
        cache_key = SessionCacheKeys.single_session(sessionId)
        async def queryDB():
            session = await self.sessionRepo.get_session_by_id(db, sessionId)
            if not session:
                AppException(status_code=404, message="Session Not Found", error= "SESSION_NOT_FOUND")
            json_session = jsonable_encoder(session)
            return json_session
        
        result = await self.redis_cache_service.get_or_set(cache_key, queryDB)
        return result
    
    async def get_user_sessions(self, db:AsyncSession,request: Request, userId:str,  query:QueryOptionsDto = Depends()):
        options = {**dict(request.query_params), **query.model_dump(exclude_none = True)}
        cache_key = SessionCacheKeys.user_sessions(userId, options)
        search_able_fields = [
            "ipAddress",
            "deviceName",
        ]
        
        filterable_fields = {
            "source" : "source",
            "deviceType": "deviceType",
            "isValid":"isValid"
        }
        queryConfig = QueryConfig(
            searchable_fields = search_able_fields,
            filterable_fields = filterable_fields,
            default_sort=  "createdAt:DESC"
        ).where(
            Session.userId == userId
        )
        
        async def queryDB():
            result = await self.sessionRepo.get_sessions_by_user_id(db, userId, options, queryConfig)
            json_result = jsonable_encoder(result)
            return json_result
        result = await self.redis_cache_service.get_or_set(cache_key, queryDB)
        return result
    
    async def get_all_sessions(self, db:AsyncSession,request: Request,  query:QueryOptionsDto = Depends()):
        options = {**dict(request.query_params), **query.model_dump(exclude_none = True)}
        cache_key = SessionCacheKeys.sessions_list(options)
        search_able_fields = [
            "ipAddress",
            "deviceName",
        ]
        
        filterable_fields = {
            "source" : "source",
            "deviceType": "deviceType",
            "isValid":"isValid",
            "userId": "userId"
        }
        queryConfig = QueryConfig(
            searchable_fields = search_able_fields,
            filterable_fields = filterable_fields,
            default_sort=  "createdAt:DESC"
        )
        
        async def queryDB():
            result = await self.sessionRepo.get_all_sessions(db, options, queryConfig)
            json_result = jsonable_encoder(result)
            return json_result
        result = await self.redis_cache_service.get_or_set(cache_key, queryDB)
        return result
            
        
        ...