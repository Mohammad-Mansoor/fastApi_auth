from core.database import Base

from sqlalchemy import (
    Column,
    String,
    Boolean,
    ForeignKey,
    DateTime,
    Enum as SQLEnum,
    UniqueConstraint
)

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from modules.sessions.models import SessionSourceTypes

import uuid


class UserDevices(Base):

    __tablename__ = "user_devices"

    __table_args__ = (
        UniqueConstraint(
            "userId",
            "deviceId",
            name="uq_user_device"
        ),
    )

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    userId = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    user = relationship(
        "User",
        back_populates="userDevices"
    )

    # DEVICE INFO
    deviceId = Column(
        String(255),
        nullable=False,
        index=True
    )

    deviceName = Column(
        String(255),
        nullable=False
    )

    deviceType = Column(
        String(100),
        nullable=True
    )

    source = Column(
        SQLEnum(SessionSourceTypes),
        nullable=False
    )

    # CLIENT INFO
    fingerprint = Column(
        String(520),
        nullable=True
    )

    userAgent = Column(
        String(520),
        nullable=True
    )

    browser = Column(
        String(255),
        nullable=True
    )

    os = Column(
        String(255),
        nullable=True
    )

    # NETWORK INFO
    lastIp = Column(
        String(255),
        nullable=True
    )

    # DEVICE STATE
    isTrusted = Column(
        Boolean,
        default=False
    )

    isActive = Column(
        Boolean,
        default=True
    )

    # ACTIVITY
    lastSeenAt = Column(
        DateTime(timezone=True),
        nullable=True
    )

    removedAt = Column(
        DateTime(timezone=True),
        nullable=True
    )

    # TIMESTAMPS
    createdAt = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updatedAt = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )