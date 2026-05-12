


from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from core.schemas import QueryOptionsDto
from modules.usersDevices.service import UserDeviceService


user_device_router = APIRouter(prefix="/devices", tags=["User Devices"])
user_service = UserDeviceService()
@user_device_router.get("/")
async def get_all_devices(request:Request, query: QueryOptionsDto = Depends(), db:AsyncSession = Depends(get_db)):
    result = await user_service.get_all_devices(db, request, query)
    return result

@user_device_router.get('/user/{userId}')
async def get_user_devices(userId:str, request:Request, query: QueryOptionsDto = Depends(), db:AsyncSession = Depends(get_db)):
    result = await user_service.get_user_devices(userId, request, db, query)
    return result
    ...
    
@user_device_router.get('/{deviceId}')
async def get_single_device(deviceId:str, db:AsyncSession = Depends(get_db)):
    result = await user_service.get_device_by_id(deviceId, db)
    return result
    ...