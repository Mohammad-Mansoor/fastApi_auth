from datetime import datetime
from uuid import UUID
from pydantic import BaseModel
from modules.users.schemas import SingleUserOut
from modules.sessions.schema import SessionOut


class LoginPayload(BaseModel):
    email: str
    password: str


class LoginResponse(BaseModel):
    success: bool
    access_token: str
    message: str
    
    
class UserNotificationOut(BaseModel):
    id: UUID
    userId: UUID
    isWhatsappOn: bool 
    isTelegramOn: bool 
    isEmailOn: bool 
    isInAppOn: bool
    createdAt: datetime
    updatedAt: datetime

    model_config = {
        "from_attributes": True
    } 
    
class UserOut(BaseModel):
    id: UUID
    firstName: str
    lastName: str
    email: str
    whatsapp: str | None = None
    telegramUsername: str | None = None
    telegramChatId: str | None = None
    telegramUserId: str | None = None
    isActive: bool
    isSuperAdmin: bool
    createdAt: datetime
    updatedAt: datetime

    notifications: UserNotificationOut | None
    model_config = {
        "from_attributes": True
    } 


class SingleUserOut(BaseModel):
    success: bool
    message: str
    data: UserOut
    cached: bool
    
class LogoutResponse(BaseModel):
    success: bool
    message: str
    
class RefreshTokenResponse(BaseModel):
    success: bool
    message: str
    access_token:str
    
class RevokeSessionResponse(BaseModel):
    success:bool
    message: str
    data: SessionOut
    


