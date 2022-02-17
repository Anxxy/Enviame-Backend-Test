from sqlalchemy import Table, Column, Integer, String, Enum, ForeignKey
from sqlalchemy import TIMESTAMP
from src.models.order.entities.enums.order_status import OrderStatus

from src.models.order.entities.order import Order

from src.shared.repositories.sqlalchemy_repository import SQLAlchemyRepository


class SQLAlchemyOrdersRepository(SQLAlchemyRepository):
    def __init__(self, client, test=False):
        table_name = "Orders"

        if test:
            table_name += "_test"

        table = Table(
            table_name,
            client.mapper_registry.metadata,
            Column("id", Integer, primary_key=True),
            Column("buyer", Integer, ForeignKey("Users.id")),
            Column("seller", Integer, ForeignKey("Sellers.id")),
            Column("quantity", String(50)),
            Column("status", Enum(OrderStatus)),

            Column("created_at", TIMESTAMP),
            Column("updated_at", TIMESTAMP),
            Column("deleted_at", TIMESTAMP, nullable=True),
        )

        super().__init__(client, Order, table, test)
