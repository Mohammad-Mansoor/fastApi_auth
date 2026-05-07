

from core.database import Base
from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid
import enum

class SessionSourceTypes(str, enum.Enum):
    WEB = "web"
    MOBILE = "mobile"
    API = "api"
    DESKTOP = "desktop"

class Session(Base):
    __tablename__ = "sessions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    userId = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)

    user = relationship("User", back_populates="sessions")

    refreshToken = Column(String(512), nullable=False, unique=True, index=True)

    ipAddress = Column(String(255), nullable=False) # e.g. "127.0.0.1"
    userAgent = Column(String(1000), nullable=False) # e.g. "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"

    deviceId = Column(String(255), nullable=False) # e.g. "1234567890 which will be used to identify the device for tracking the new device login"
    deviceName = Column(String(255), nullable=False) # e.g. "iPhone 14 Pro Max"
    deviceType = Column(String(255), nullable=False) # e.g. "mobile" OR "desktop"

    os = Column(String(255), nullable=False) # e.g. "iOS"
    browser = Column(String(255), nullable=True) # e.g. "Chrome"

    source = Column(SQLEnum(SessionSourceTypes), nullable=False) # e.g. "web BROWSER" OR "mobile APP" OR "api CALL" OR "desktop APP"

    fingerprint = Column(String(512), nullable=False, index=True) # e.g. "1234567890"

    isValid = Column(Boolean, nullable=False, default=True, index=True) # e.g. True or False

    expiresAt = Column(DateTime(timezone=True), nullable=False, index=True) # e.g. 2026-05-04 12:00:00
    lastActiveAt = Column(DateTime(timezone=True), nullable=False) # e.g. 2026-05-04 12:00:00

    logoutAt = Column(DateTime(timezone=True), nullable=True) # e.g. 2026-05-04 12:00:00
    revokeAt = Column(DateTime(timezone=True), nullable=True) # e.g. 2026-05-04 12:00:00
    revokeReason = Column(String(255), nullable=True) # e.g. "User logged out"

    createdAt = Column(DateTime(timezone=True), server_default=func.now()) # e.g. 2026-05-04 12:00:00
    updatedAt = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now()) # e.g. 2026-05-04 12:00:00