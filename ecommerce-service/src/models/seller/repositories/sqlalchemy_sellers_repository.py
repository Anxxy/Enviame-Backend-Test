from sqlalchemy import Table, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import TIMESTAMP
from src.models.seller.entities.seller import Seller

from src.shared.repositories.sqlalchemy_repository import SQLAlchemyRepository


class SQLAlchemySellersRepository(SQLAlchemyRepository):
    def __init__(self, sqlalchemy_client, test=False):
        table_name = "Sellers"

        if test:
            table_name += "_test"

        table = Table(
            table_name,
            sqlalchemy_client.mapper_registry.metadata,
            Column("id", Integer, primary_key=True),
            Column("name", String(50)),
            Column("description", String(100)),
            Column("user", Integer),
            Column("created_at", TIMESTAMP),
            Column("updated_at", TIMESTAMP),
            Column("deleted_at", TIMESTAMP, nullable=True),
        )
        
        super().__init__(sqlalchemy_client, Seller, table, test)
