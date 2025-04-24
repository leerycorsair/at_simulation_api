import enum
from typing import Any, List

from sqlalchemy import (
    JSON,
    Boolean,
    Enum,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship

from at_simulation_api.schema.base import Base


class ResourceTypeTypeEnum(enum.Enum):
    CONSTANT = "CONSTANT"
    TEMPORAL = "TEMPORAL"


class ResourceType(Base):
    __tablename__ = "resource_types"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    name: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )
    type: Mapped[ResourceTypeTypeEnum] = mapped_column(
        Enum(ResourceTypeTypeEnum),
        nullable=False,
    )
    model_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("models.id"),
        nullable=False,
    )

    attributes = relationship(
        "ResourceTypeAttribute",
        cascade="all, delete-orphan",
    )
    resources = relationship(
        "Resource",
        cascade="all, delete-orphan",
    )
    rel_resources = relationship(
        "RelevantResource",
        cascade="all, delete-orphan",
    )

    __table_args__ = (
        UniqueConstraint(
            "name",
            "model_id",
            name="uix_resource_type_name_model_id",
        ),
    )


class ResourceTypeAttribute(Base):
    __tablename__ = "resource_type_attributes"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    name: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )
    type: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )
    default_value: Mapped[Any] = mapped_column(
        JSON,
        nullable=True,
    )
    enum_values_set: Mapped[List[str]] = mapped_column(
        ARRAY(String),
        nullable=True,
    )
    resource_type_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("resource_types.id"),
        nullable=False,
    )
    resource_attributes = relationship(
        "ResourceAttribute",
        cascade="all, delete-orphan",
    )

    __table_args__ = (
        UniqueConstraint(
            "name",
            "resource_type_id",
            name="uix_resource_type_attribute_name_resource_type_id",
        ),
    )


class Resource(Base):
    __tablename__ = "resources"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    name: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )
    to_be_traced: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
    )
    resource_type_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("resource_types.id"),
        nullable=False,
    )
    model_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("models.id"),
        nullable=False,
    )

    attributes = relationship(
        "ResourceAttribute",
        cascade="all, delete-orphan",
    )
    usage_resources = relationship(
        "TemplateUsageArgument",
        cascade="all, delete-orphan",
    )

    __table_args__ = (
        UniqueConstraint(
            "name",
            "model_id",
            name="uix_resource_name_model_id",
        ),
    )


class ResourceAttribute(Base):
    __tablename__ = "resource_attributes"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    value: Mapped[Any] = mapped_column(
        JSON,
        nullable=False,
    )
    resource_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("resources.id"),
        nullable=False,
    )
    rta_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("resource_type_attributes.id"),
        nullable=False,
    )
