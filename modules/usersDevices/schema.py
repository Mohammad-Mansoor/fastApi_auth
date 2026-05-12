from datetime import datetime
from pydantic import BaseModel

from modules.sessions.models import SessionSourceTypes



class AddDevice(BaseModel):
    userId: str
    deviceId: str
    deviceName:str
    deviceType:str
    source: SessionSourceTypes
    fingerprint: str
    userAgent: str
    browser:str
    os: str
    lastIp: str
    isTrusted: bool = False
    isActive:bool = True
    lastSeenAt: datetime = datetime.utcnow()
    