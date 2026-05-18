from enum import Enum


class StorageProviderEnum(str, Enum):
    LOCAL = "local"
    S3 = "s3"
    MINIO = "minio"