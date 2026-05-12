from sqlalchemy import select, or_, and_
from sqlalchemy.ext.asyncio import AsyncSession
from common.query_builder.query_builder import SQLAlchemyQueryHelper,QueryConfig
from modules.usersDevices.schema import AddDevice
from .models import UserDevices


class UserDeviceRepository:
    async def add_device(self, db:AsyncSession, data: AddDevice):
        device = UserDevices(**data.model_dump())
        db.add(device)
        return device
    
    async def get_single_device(self, db:AsyncSession, deviceId:str):
        device = db.execute(select(UserDevices).where(UserDevices.id == deviceId))
        return device.scalars().first()

    async def get_all_devices(self, db:AsyncSession, query:dict, queryConfig):
        result = SQLAlchemyQueryHelper.for_(
            model = UserDevices,
            session = db,
            options = query,
            config = queryConfig
        )
        response = await result.get_many_and_meta()
        return response
    
    async def get_user_devices(self, db:AsyncSession,userId:str, query:dict, queryConfig):
        result = SQLAlchemyQueryHelper.for_(
            model = UserDevices,
            session = db,
            options = query,
            config = queryConfig
        )
        response = await result.get_many_and_meta()
        return response
    
    async def find_device(self, db:AsyncSession,user_id:str, device_id:str, fingerprint:str):
        """
        Resolve device using:
        1. userId + deviceId (primary)
        2. userId + fingerprint (fallback)
        """

        # ----------------------------
        # STEP 1: deviceId match (strong identity)
        # ----------------------------
        if device_id:
            result = await db.execute(
                select(UserDevices).where(
                    and_(
                        UserDevices.userId == user_id,
                        UserDevices.deviceId == device_id
                    )
                )
            )
            device = result.scalars().first()

            if device:
                return device

        # ----------------------------
        # STEP 2: fingerprint fallback (weak identity)
        # ----------------------------
        if fingerprint:
            result = await db.execute(
                select(UserDevices).where(
                    and_(
                        UserDevices.userId == user_id,
                        UserDevices.fingerprint == fingerprint
                    )
                )
            )
            device = result.scalars().first()

            if device:
                return device

        # ----------------------------
        # STEP 3: no match → new device
        # ----------------------------
        return None   
        ...
    
