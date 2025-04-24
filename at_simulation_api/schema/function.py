from sqlalchemy import ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from at_simulation_api.schema.base import Base


class Function(Base):
    __tablename__ = "functions"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    name: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )
    ret_type: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )
    body: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    parameters = relationship(
        "FunctionParameter",
        cascade="all, delete-orphan",
    )
    model_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("models.id"),
        nullable=False,
    )

    __table_args__ = (
        UniqueConstraint(
            "name",
            "model_id",
            name="uix_function_name_model_id",
        ),
    )


class FunctionParameter(Base):
    __tablename__ = "function_parameters"

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

    function_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("functions.id"),
        nullable=False,
    )

    __table_args__ = (
        UniqueConstraint(
            "name",
            "function_id",
            name="uix_function_parameter_function",
        ),
    )
