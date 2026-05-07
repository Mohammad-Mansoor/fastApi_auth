from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
import uuid
from uuid import UUID

# 🔹 Create User
class UserCreate(BaseModel):
    firstName: str
    lastName: str
    email: EmailStr

    whatsapp: Optional[str] = None
    telegramUsername: Optional[str] = None
    telegramChatId: Optional[str] = None
    telegramUserId: Optional[str] = None

    isActive: bool = True
    isSuperAdmin: bool = False


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

# 🔹 Response
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

    


class CreateUserResponse(BaseModel):
    success: bool
    message: str
    data: UserOut

class UserNotificationCreate(BaseModel):
    userId: UUID
    isWhatsappOn: bool = False
    isTelegramOn: bool = False
    isEmailOn: bool = True
    isInAppOn: bool = True





# UserOut.model_rebuild()