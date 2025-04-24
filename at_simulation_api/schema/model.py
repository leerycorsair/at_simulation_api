from datetime import datetime

from sqlalchemy import TIMESTAMP, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from at_simulation_api.schema.base import Base


class Model(Base):
    __tablename__ = "models"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    name: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )
    user_id: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        nullable=False,
        default=datetime.now(),
    )

    nodes = relationship(
        "Node",
        cascade="all, delete-orphan",
    )
    edges = relationship(
        "Edge",
        cascade="all, delete-orphan",
    )
    resource_types = relationship(
        "ResourceType",
        cascade="all, delete-orphan",
    )
    resources = relationship(
        "Resource",
        cascade="all, delete-orphan",
    )
    functions = relationship(
        "Function",
        cascade="all, delete-orphan",
    )
    templates = relationship(
        "Template",
        cascade="all, delete-orphan",
    )
    template_usages = relationship(
        "TemplateUsage",
        cascade="all, delete-orphan",
    )
    imports = relationship(
        "Import",
        cascade="all, delete-orphan",
    )

    __table_args__ = (
        UniqueConstraint(
            "name",
            "user_id",
            name="uix_model_name_user_id",
        ),
    )
