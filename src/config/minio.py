import argparse
import os
from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings

def parse_args():
    parser = argparse.ArgumentParser(description="Minio configuration.")
    parser.add_argument('--MINIO_HOST', type=str, help="Minio host.")
    parser.add_argument('--MINIO_ACCESS_KEY', type=str, help="Minio access key.")
    parser.add_argument('--MINIO_SECRET_KEY', type=str, help="Minio secret key.")
    parser.add_argument('--MINIO_SECURE', type=bool, help="Use secure connection.")
    parser.add_argument('--MINIO_BUCKET_NAME', type=str, help="Minio bucket name.")
    parser.add_argument('--MINIO_API_PORT', type=int, help="Minio API port.")
    parser.add_argument('--MINIO_CONSOLE_PORT', type=int, help="Minio console port.")
    return parser.parse_args()

class MinioConfig(BaseSettings):
    host: str = Field(..., alias="MINIO_HOST")
    access_key: str = Field(..., alias="MINIO_ACCESS_KEY")
    secret_key: str = Field(..., alias="MINIO_SECRET_KEY")
    secure: bool = Field(..., alias="MINIO_SECURE")
    bucket_name: str = Field(..., alias="MINIO_BUCKET_NAME")
    api_port: int = Field(..., alias="MINIO_API_PORT")
    console_port: int = Field(..., alias="MINIO_CONSOLE_PORT")

    @property
    def endpoint(self) -> str:
        return f"{self.host}:{self.api_port}"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

class MinioStore:
    @classmethod
    @lru_cache(maxsize=1)
    def get_minio_config(cls) -> MinioConfig:
        args = parse_args()
        
        if args.MINIO_HOST:
            os.environ["MINIO_HOST"] = args.MINIO_HOST
        if args.MINIO_ACCESS_KEY:
            os.environ["MINIO_ACCESS_KEY"] = args.MINIO_ACCESS_KEY
        if args.MINIO_SECRET_KEY:
            os.environ["MINIO_SECRET_KEY"] = args.MINIO_SECRET_KEY
        if args.MINIO_SECURE is not None:
            os.environ["MINIO_SECURE"] = str(args.MINIO_SECURE)
        if args.MINIO_BUCKET_NAME:
            os.environ["MINIO_BUCKET_NAME"] = args.MINIO_BUCKET_NAME
        if args.MINIO_API_PORT:
            os.environ["MINIO_API_PORT"] = str(args.MINIO_API_PORT)
        if args.MINIO_CONSOLE_PORT:
            os.environ["MINIO_CONSOLE_PORT"] = str(args.MINIO_CONSOLE_PORT)
        
        config = MinioConfig()
        
        if not config.host or not config.access_key or not config.secret_key or not config.bucket_name:
            raise ValueError("Minio configuration is missing required values.")
        
        return config
