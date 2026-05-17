from datetime import datetime
from pydantic import BaseModel
# from sqlalchemy import UUID
from .models import SessionSourceTypes
from uuid import UUID



class CreateSession(BaseModel):
    userId: UUID
    refreshToken: str
    ipAddress: str
    userAgent: str
    deviceId: str
    deviceName: str
    deviceType: str
    os: str
    browser: str
    source: SessionSourceTypes
    fingerprint: str
    isValid: bool  = True
    expiresAt: datetime
    lastActiveAt: datetime = datetime.utcnow()
    
    
class SessionOut(BaseModel):
    userId: UUID
    ipAddress: str
    userAgent: str
    deviceId: str
    deviceName: str
    deviceType: str
    os: str
    browser: str
    source: SessionSourceTypes
    fingerprint: str
    isValid: bool  = True
    expiresAt: datetime
    lastActiveAt: datetime = datetime.utcnow()
    logoutAt: datetime
    revokeAt: datetime
    createdAt: datetime
    updatedAt: datetime
    revokeReason:str
    