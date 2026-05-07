

from core.database import Base
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    firstName = Column(String(255), nullable=False)
    lastName = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True, index=True)
    password = Column(String(255), nullable=False)
    whatsapp = Column(String(255), nullable=True, unique=True, index=True)
    telegramUsername = Column(String(255), nullable=True, unique=True, index=True)
    telegramChatId = Column(String(255), nullable=True, unique=True, index=True)
    telegramUserId = Column(String(255), nullable=True, unique=True, index=True)
    notifications = relationship("UserNotifications", back_populates="user", cascade="all, delete-orphan", uselist=False, lazy="joined")
    sessions = relationship("Session", back_populates = "user", cascade="all, delete-orphan")
    userDevices = relationship("UserDevices", back_populates = "user", cascade="all, delete-orphan")

    createdAt = Column(DateTime, server_default=func.now())
    updatedAt = Column(DateTime, server_default=func.now(), onupdate=func.now())

    isActive = Column(Boolean, nullable=False, default=True)
    isSuperAdmin = Column(Boolean, nullable=False, default=False)




class UserNotifications(Base):
    __tablename__ = "user_notifications"
    id = Column(UUID(as_uuid = True), primary_key=True, default = uuid.uuid4)
    userId = Column(UUID(as_uuid = True), ForeignKey("users.id"), nullable=False, index=True, unique=True)
    user = relationship("User", back_populates="notifications")
    isWhatsappOn = Column(Boolean, nullable=False, default=False)
    isTelegramOn = Column(Boolean, nullable=False, default=False)
    isEmailOn = Column(Boolean, nullable=False, default=True)
    isInAppOn = Column(Boolean, nullable=False, default=True)

    createdAt = Column(DateTime, server_default=func.now())
    updatedAt = Column(DateTime, server_default=func.now(), onupdate=func.now())

