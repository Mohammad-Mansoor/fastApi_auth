import uuid

from sqlalchemy import (
    Column,
    String,
    BigInteger,
    Boolean,
    DateTime,
    ForeignKey,
    Text,
    Enum as SQLEnum,
    Index,
)

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func


from core.database import Base

from modules.files.enums.file_status_enum import FileStatusEnum
from modules.files.enums.storage_provider_enum import StorageProviderEnum
from modules.files.enums.reference_type_enum import ReferenceTypeEnum


class File(Base):
    __tablename__ = "files"

    __table_args__ = (
        # Composite index for ERP attachment queries
        Index(
            "idx_files_reference",
            "reference_type",
            "reference_id",
        ),

        # Query optimization indexes
        Index("idx_files_uploaded_by", "uploaded_by"),
        Index("idx_files_status", "status"),
        Index("idx_files_checksum", "checksum"),
    )

    # Primary UUID
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    # Original filename uploaded by user
    original_name = Column(
        String,
        nullable=False,
    )

    # Internally generated filename
    stored_name = Column(
        String,
        nullable=False,
        unique=True,
    )

    # Storage provider
    storage_provider = Column(
        SQLEnum(StorageProviderEnum),
        nullable=False,
        default=StorageProviderEnum.LOCAL,
    )

    # Bucket name (S3/MinIO)
    bucket_name = Column(
        String,
        nullable=True,
    )

    # Physical storage path / object key
    storage_path = Column(
        Text,
        nullable=False,
    )

    # File metadata
    mime_type = Column(
        String,
        nullable=False,
    )

    extension = Column(
        String,
        nullable=True,
    )

    size = Column(
        BigInteger,
        nullable=False,
    )

    # SHA256 checksum
    checksum = Column(
        String,
        nullable=True,
    )

    # ERP attachment relation
    reference_type = Column(
        SQLEnum(ReferenceTypeEnum),
        nullable=True,
    )

    reference_id = Column(
        String,
        nullable=True,
    )

    # Public/private access
    is_public = Column(
        Boolean,
        default=False,
    )

    # File lifecycle status
    status = Column(
        SQLEnum(FileStatusEnum),
        nullable=False,
        default=FileStatusEnum.UPLOADED,
    )

    # Soft delete
    is_deleted = Column(
        Boolean,
        default=False,
    )

    # Uploaded by user
    uploaded_by = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=True,
    )

    # Audit timestamps
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    updated_at = Column(
        DateTime(timezone=True),
        onupdate=func.now(),
    )

    deleted_at = Column(
        DateTime(timezone=True),
        nullable=True,
    )