import enum

from sqlalchemy import Enum, Float, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from at_simulation_api.schema.base import Base


class TemplateTypeEnum(enum.Enum):
    IRREGULAR_EVENT = "IRREGULAR_EVENT"
    OPERATION = "OPERATION"
    RULE = "RULE"


class Template(Base):
    __tablename__ = "templates"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    name: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )
    type: Mapped[TemplateTypeEnum] = mapped_column(
        Enum(TemplateTypeEnum),
        nullable=False,
    )

    model_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("models.id"),
        nullable=False,
    )
    relevant_resources = relationship(
        "RelevantResource",
        cascade="all, delete-orphan",
    )
    template_usages = relationship(
        "TemplateUsage",
        cascade="all, delete-orphan",
    )
    irregular_event_bodies = relationship(
        "IrregularEventBody",
        cascade="all, delete-orphan",
    )
    irregular_event_generators = relationship(
        "IrregularEventGenerator",
        cascade="all, delete-orphan",
    )
    operation_bodies = relationship(
        "OperationBody",
        cascade="all, delete-orphan",
    )
    rule_bodies = relationship(
        "RuleBody",
        cascade="all, delete-orphan",
    )

    __table_args__ = (
        UniqueConstraint(
            "name",
            "model_id",
            name="uix_template_name_model_id",
        ),
    )


class RelevantResource(Base):
    __tablename__ = "relevant_resources"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    name: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    template_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("templates.id"),
        nullable=False,
    )
    resource_type_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("resource_types.id"),
        nullable=False,
    )
    
    template_usage_args = relationship(
        "TemplateUsageArgument",
        cascade="all, delete-orphan",
    )

    __table_args__ = (
        UniqueConstraint(
            "name",
            "template_id",
            name="uix_relevant_resource_name_template_id",
        ),
    )


class TemplateUsage(Base):
    __tablename__ = "template_usages"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    name: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )
    template_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("templates.id"),
        nullable=False,
    )
    model_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("models.id"),
        nullable=False,
    )
    
    template_usage_args = relationship(
        "TemplateUsageArgument",
        cascade="all, delete-orphan",
    )

    __table_args__ = (
        UniqueConstraint(
            "name",
            "model_id",
        ),
    )


class TemplateUsageArgument(Base):
    __tablename__ = "template_usage_args"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    relevant_resource_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("relevant_resources.id"),
        nullable=False,
    )
    template_usage_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("template_usages.id"),
        nullable=False,
    )
    resource_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("resources.id"),
        nullable=False,
    )


class IrregularEventBody(Base):
    __tablename__ = "irregular_event_bodies"

    body: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    template_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("templates.id"),
        primary_key=True,
        nullable=False,
    )


class IrregularEventGeneratorTypeEnum(enum.Enum):
    NORMAL = "NORMAL"
    PRECISE = "PRECISE"
    UNIFORM = "UNIFORM"
    EXPONENTIAL = "EXPONENTIAL"
    GAUSSIAN = "GAUSSIAN"
    POISSON = "POISSON"


class IrregularEventGenerator(Base):
    __tablename__ = "irregular_event_generators"

    type: Mapped[IrregularEventGeneratorTypeEnum] = mapped_column(
        Enum(IrregularEventGeneratorTypeEnum),
        nullable=False,
    )
    value: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )
    dispersion: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )
    template_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("templates.id"),
        primary_key=True,
        nullable=False,
    )


class OperationBody(Base):
    __tablename__ = "operation_bodies"

    condition: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    body_before: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    delay: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    body_after: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    template_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("templates.id"),
        primary_key=True,
        nullable=False,
    )


class RuleBody(Base):
    __tablename__ = "rule_bodies"

    condition: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    body: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    template_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("templates.id"),
        primary_key=True,
        nullable=False,
    )
