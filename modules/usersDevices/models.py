from core.database import Base
from sqlalchemy import Column, String, Boolean, ForeignKey, DateTime, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from modules.users.models import User
import uuid
import enum




class UserDevices(Base):
    __tablename__ = "user_devices"

    id = Column(UUID(as_uuid=True), primary_key = True, default = uuid.uuid4)
    userId  = Column(UUID(as_uuid= True), ForeignKey("users.id"), nullable=False, index  = True)
    user = relationship("User", back_populates = "userDevices")
    deviceId = Column(String(255), nullable=False, index=True)
    deviceType = Column(String(255), nullable=True)
    fingerprint = Column(String(520), nullable=True)
    userAgent = Column(String(520), nullable=True)
    borwser = Column(String(520), nullable=True)
    os = Column(String(255), nullable=True)
    lastIp = Column(String(255), nullable=True)
    createdAt = Column(DateTime, server_default = func.now())
    updatedAt = Column(DateTime, server_default = func.now(), onupdate = func.now())
