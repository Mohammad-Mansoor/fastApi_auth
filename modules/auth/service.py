from sqlalchemy.ext.asyncio import AsyncSession
from core.security import verify_password, create_access_token, create_refresh_token
from .schemas import LoginPayload
from core.schemas import Headers
from modules.users.repository import UserRepository
from core.exceptions.app_exception import AppException



class AuthService:
    def __init__(self):
        self.userRepo = UserRepository()

    async def login(self, db:AsyncSession, data: LoginPayload):
        user = await self.userRepo.get_user_by_email(db, data.email)
        print(user)

        if not user:
            raise AppException(status_code=400, message = "Invalid Email or password", error ="Invalid Email or password")

        if not verify_password(data.password, user.password):
            raise AppException(status_code=400, message = "Invalid Email or password", error ="Invalid Email or password")
        
        access_token_payload ={
            "userId": str(user.id)
            
        }
        access_token = create_access_token(access_token_payload)
        return {
            "success": True,
            "message": "Login Successful",
            "access_token": access_token
        }
        

