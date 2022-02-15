from sqlalchemy import Table, Column, Integer, String, Enum
from sqlalchemy.orm import relationship
from sqlalchemy import TIMESTAMP

from src.models.product.entities.product import Product

from src.shared.repositories.sqlalchemy_repository import SQLAlchemyRepository


class SQLAlchemyProductsRepository(SQLAlchemyRepository):
    def __init__(self, client, test=False):
        table_name = "Products"

        if test:
            table_name += "_test"

        table = Table(
            table_name,
            client.mapper_registry.metadata,
            Column("id", Integer, primary_key=True),
            Column("name", String(50)),
            Column("description", String(50)),
            Column("quantity", Integer),

            Column("created_at", TIMESTAMP),
            Column("updated_at", TIMESTAMP),
            Column("deleted_at", TIMESTAMP, nullable=True),
        )

        super().__init__(client, Product, table, test)
