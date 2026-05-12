import uuid
from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession
from core.security import verify_password, create_access_token, create_refresh_token
from modules.usersDevices.repository import UserDeviceRepository
from .schemas import LoginPayload
from core.schemas import Headers
from modules.users.repository import UserRepository
from modules.sessions.repository import SessionRepository
from core.exceptions.app_exception import AppException
from modules.sessions.schema import CreateSession
from modules.usersDevices.schema import AddDevice
from common.utils.session_helper import SessionHelper
from core.exceptions.app_exception import AppException



class AuthService:
    def __init__(self):
        self.userRepo = UserRepository()
        self.sessionRepo = SessionRepository()
        self.deviceRepo = UserDeviceRepository()

    async def login(self, db:AsyncSession, data: LoginPayload, request: Request):
        user = await self.userRepo.get_user_by_email(db, data.email)
        print(user)

        if not user:
            raise AppException(status_code=400, message = "Invalid Email or password", error ="Invalid Email or password")

        if not verify_password(data.password, user.password):
            raise AppException(status_code=400, message = "Invalid Email or password", error ="Invalid Email or password")
        
        existing_device_id = SessionHelper.get_device_id_from_cookies(request)
        incoming_finger_print = SessionHelper.get_fingerprint(request)
        find_device = await self.deviceRepo.find_device(db, user.id, existing_device_id, incoming_finger_print)
        refresh_token_payload = {
            "userId": str(user.id)
        }
        refresh_token = create_refresh_token(refresh_token_payload)
        session_payload = SessionHelper.build_session_payload(
            request = request,
            user_id = user.id,
            refresh_token=refresh_token
        )
        device_payload = SessionHelper.build_device_payload(session_payload)

        if not find_device:
            device = await self.deviceRepo.add_device(db, device_payload)
            existing_device_id = str(uuid.uuid4())
            print("New Device Detected device_id❌❌❌", existing_device_id)
            #ALERT THE USER VIA PREFERED NOTIFICATION CHANNEL
        else:
            print("No New Device Detected device_id ✅✅✅", existing_device_id)
            #UPDATE THE DEVIEC INFO.
            ...
            
        session = await self.sessionRepo.create_session(db, session_payload)
        # device = await self.deviceRepo.add_device(db,device_payload)
        
        access_token_payload ={
            "userId": str(user.id),
            "sessionId": str(session.id)
        }
        access_token = create_access_token(access_token_payload)
        await db.commit()
        
        return {
            "refresh_token": refresh_token,
            "access_token": access_token,
            "device_id": existing_device_id
            
        }
        
    async def me(self, db:AsyncSession, request:Request):
        user_id = request.state.userId
        if not user_id:
            raise AppException(status_code=404, message= "Not Found", error= "NOT_FOUND")
        
        user = await self.userRepo.get_user_by_id(db, user_id)
        return user
