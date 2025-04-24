from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase

metadata = MetaData()
Base = DeclarativeBase(metadata=metadata)
