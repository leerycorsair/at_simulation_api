import argparse
import os
from functools import lru_cache
from pydantic import BaseSettings, Field
from pydantic_settings import BaseSettings

def parse_args():
    parser = argparse.ArgumentParser(description="Database configuration.")
    parser.add_argument('--DB_HOST', type=str, help="Database host.")
    parser.add_argument('--DB_PORT', type=int, help="Database port.")
    parser.add_argument('--DB_NAME', type=str, help="Database name.")
    parser.add_argument('--DB_USER', type=str, help="Database user.")
    parser.add_argument('--DB_PASS', type=str, help="Database password.")
    return parser.parse_args()

class DatabaseConfig(BaseSettings):
    host: str = Field(..., alias="DB_HOST")
    port: int = Field(..., alias="DB_PORT")
    name: str = Field(..., alias="DB_NAME")
    user: str = Field(..., alias="DB_USER")
    password: str = Field(..., alias="DB_PASS")

    @property
    def url(self) -> str:
        return f"postgresql+psycopg2://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

class PostgresStore:
    @classmethod
    @lru_cache(maxsize=1)
    def get_database_config(cls) -> DatabaseConfig:
        args = parse_args()
        
        if args.DB_HOST:
            os.environ["DB_HOST"] = args.DB_HOST
        if args.DB_PORT:
            os.environ["DB_PORT"] = str(args.DB_PORT)
        if args.DB_NAME:
            os.environ["DB_NAME"] = args.DB_NAME
        if args.DB_USER:
            os.environ["DB_USER"] = args.DB_USER
        if args.DB_PASS:
            os.environ["DB_PASS"] = args.DB_PASS
        
        config = DatabaseConfig()
        
        if not config.host or not config.port or not config.name or not config.user or not config.password:
            raise ValueError("Database configuration is missing required values.")
        
        return config

