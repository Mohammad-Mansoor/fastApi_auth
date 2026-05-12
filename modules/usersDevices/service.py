from modules.usersDevices.models import UserDevices
from modules.usersDevices.repository import UserDeviceRepository
from fastapi import Depends, Request
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from common.query_builder.query_builder import QueryConfig
from core.exceptions.app_exception import AppException
from core.schemas import QueryOptionsDto
from infrastructure.redis.service import RedisCacheService
from infrastructure.redis.keys import UserDeviceCacheKeys
from modules.usersDevices.schema import AddDevice


class UserDeviceService:
    def __init__(self):
        self.userDeviceRepo = UserDeviceRepository()
        self.redis_cache_service = RedisCacheService()
        
    async def get_all_devices(self, db:AsyncSession,request:Request, query: QueryOptionsDto = Depends() ):

        options = {
            **dict(request.query_params),
            **query.model_dump(exclude_none=True)
        }
        
        cache_key = UserDeviceCacheKeys.users_devices_list(options)
        
        filterable_fields = {
            "source" : "source",
            "deviceType": "deviceType",
            "isActive":"isActive",
            "os":"os",
            "isTrusted":"isTrusted"
        }
        
        search_able_fields = [
            "ipAddress",
            "deviceName",
            "browser"
        ]
        
        queryConfig = QueryConfig(
            searchable_fields= search_able_fields,
            filterable_fields= filterable_fields,
            default_sort= "createdAt:DESC"
        )
        
        async def queryDB():
            result = await self.userDeviceRepo.get_all_devices(db, options, queryConfig)
            json_result = jsonable_encoder(result)
            return json_result
        
        result = await self.redis_cache_service.get_or_set(cache_key, queryDB)
        return result
        
        ...
        
    async def get_user_devices(self,userId:str, request:Request, db:AsyncSession, query:QueryOptionsDto = Depends() ):
        options = {
            **dict(request.query_params),
            **query.model_dump(exclude_none=True)
        }
        cache_key = UserDeviceCacheKeys.user_base_devices(userId)
        filterable_fields = {
            "source" : "source",
            "deviceType": "deviceType",
            "isActive":"isActive",
            "os":"os",
            "isTrusted":"isTrusted"
        }
        
        search_able_fields = [
            "ipAddress",
            "deviceName",
            "browser"
        ]
        
        queryConfig = QueryConfig(
            searchable_fields= search_able_fields,
            filterable_fields= filterable_fields,
            default_sort= "createdAt:DESC"
        ).where(
            UserDevices.userId == userId
        )
        
        async def queryDB():
            result = await self.userDeviceRepo.get_user_devices(db,userId, options, queryConfig)
            json_result = jsonable_encoder(result)
            return json_result
        
        result = await self.redis_cache_service.get_or_set(cache_key, queryDB)
        return result
        
        ...
        
    async def get_device_by_id(self, deviceId:str, db:AsyncSession):
        result = await self.userDeviceRepo.get_single_device(db, deviceId)
        if not result:
            raise AppException(status_code=400, message= "Device NotFound", error="DEVICE_NOT_FOUND")
        return result