from datetime import datetime

from sqlalchemy import (
    TIMESTAMP,
    UUID,
    Column,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

from .base import Base


class Model(Base):
    __tablename__ = "models"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    user_id = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, default=datetime.now())

    nodes = relationship("Node", cascade="all, delete-orphan")
    edges = relationship("Edge", cascade="all, delete-orphan")
    resource_types = relationship("ResourceType", cascade="all, delete-orphan")
    resources = relationship("Resource", cascade="all, delete-orphan")
    functions = relationship("Function", cascade="all, delete-orphan")
    templates = relationship("Template", cascade="all, delete-orphan")
    template_usages = relationship("TemplateUsage", cascade="all, delete-orphan")
    imports = relationship("Import", cascade="all, delete-orphan")

    __table_args__ = (
        UniqueConstraint(
            "name",
            "user_id",
            name="uix_model_name_user_id",
        ),
    )

class TranslatedModels(Base):
    __tablename__ = "translated_models"
    
    file_uuid = Column(UUID, primary_key=True)
    file_name = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, default=datetime.now())
    
    model_id = Column(Integer, ForeignKey("models.id"), nullable=False)
