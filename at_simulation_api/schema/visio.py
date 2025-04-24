import enum

from sqlalchemy import CheckConstraint, Enum, ForeignKey, Integer, String, event
from sqlalchemy.engine import Connection
from sqlalchemy.orm import Mapped, mapped_column, relationship

from at_simulation_api.schema.base import Base
from at_simulation_api.schema.function import Function
from at_simulation_api.schema.resource import Resource, ResourceType
from at_simulation_api.schema.template import Template, TemplateUsage


class NodeType(enum.Enum):
    RESOURCE = "RESOURCE"
    RESOURCE_TYPE = "RESOURCE_TYPE"
    FUNCTION = "FUNCTION"

    RULE_TEMPLATE = "RULE_TEMPLATE"
    RULE_USAGE = "RULE_USAGE"

    OPERATION_TEMPLATE = "OPERATION_TEMPLATE"
    OPERATION_USAGE = "OPERATION_USAGE"

    IRREGULAR_TEMPLATE = "IRREGULAR_TEMPLATE"
    IRREGULAR_USAGE = "IRREGULAR_USAGE"


class Node(Base):
    __tablename__ = "nodes"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    object_table: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )
    object_name: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )
    object_id: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    node_type: Mapped[NodeType] = mapped_column(
        Enum(NodeType),
        nullable=False,
    )
    pos_x: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    pos_y: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    width: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    height: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    color: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )
    model_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("models.id"),
        nullable=False,
    )

    edges_from = relationship(
        "Edge", cascade="all, delete-orphan", foreign_keys="[Edge.from_node]"
    )
    edges_to = relationship(
        "Edge", cascade="all, delete-orphan", foreign_keys="[Edge.to_node]"
    )


def delete_associated_node(mapper, connection: Connection, target):
    node_ids = connection.execute(
        Node.__table__.select()
        .with_only_columns(Node.id)
        .where(Node.object_table == target.__tablename__)
        .where(Node.object_id == target.id)
    ).fetchall()

    node_ids = [row[0] for row in node_ids]

    if node_ids:
        connection.execute(
            Edge.__table__.delete().where(
                Edge.from_node.in_(node_ids) | Edge.to_node.in_(node_ids)
            )
        )

        connection.execute(Node.__table__.delete().where(Node.id.in_(node_ids)))


event.listen(Resource, "after_delete", delete_associated_node)
event.listen(ResourceType, "after_delete", delete_associated_node)
event.listen(Template, "after_delete", delete_associated_node)
event.listen(TemplateUsage, "after_delete", delete_associated_node)
event.listen(Function, "after_delete", delete_associated_node)


class Edge(Base):
    __tablename__ = "edges"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    from_node: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("nodes.id"),
        nullable=False,
    )
    to_node: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("nodes.id"),
        nullable=False,
    )
    model_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("models.id"),
        nullable=False,
    )

    from_node_relation = relationship(
        "Node",
        foreign_keys=[from_node],
        cascade="all, delete",
    )
    to_node_relation = relationship(
        "Node",
        foreign_keys=[to_node],
        cascade="all, delete",
    )

    __table_args__ = (
        CheckConstraint(
            "from_node != to_node",
            name="check_from_node_to_node_diff",
        ),
    )
