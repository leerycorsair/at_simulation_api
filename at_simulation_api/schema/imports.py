from sqlalchemy import ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from at_simulation_api.schema.base import Base


class Import(Base):
    __tablename__ = "imports"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    name: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )
    version: Mapped[str] = mapped_column(
        String,
        nullable=True,
    )
    model_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("models.id"),
        nullable=False,
    )
    
    packages = relationship(
        "Package",
        cascade="all, delete-orphan",
    )

    __table_args__ = (
        UniqueConstraint(
            "name",
            "model_id",
            name="uix_import_name_model_id",
        ),
    )


class Package(Base):
    __tablename__ = "packages"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    name: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )
    alias: Mapped[str] = mapped_column(
        String,
        nullable=True,
    )

    import_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("imports.id"),
        nullable=False,
    )

    __table_args__ = (
        UniqueConstraint(
            "name",
            "import_id",
            name="uix_package_name_import_id",
        ),
        UniqueConstraint(
            "alias",
            "import_id",
            name="uix_package_alias_import_id",
        ),
    )
