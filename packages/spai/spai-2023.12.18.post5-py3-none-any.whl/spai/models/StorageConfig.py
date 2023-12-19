from pydantic import BaseModel


class StorageConfig(BaseModel):
    name: str = "storage"


class LocalStorageConfig(StorageConfig):
    type: str = "local"
    path: str = "data"


class S3StorageCredentials(BaseModel):
    url: str
    access_key: str
    secret_key: str
    region: str = "us-east-1"
    bucket: str


class S3StorageConfig(StorageConfig):
    credentials: S3StorageCredentials
