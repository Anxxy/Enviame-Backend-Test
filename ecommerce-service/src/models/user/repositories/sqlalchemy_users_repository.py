from sqlalchemy import Table, Column, Integer, String, Enum
from sqlalchemy.orm import relationship
from sqlalchemy import TIMESTAMP

from src.models.user.entities.user import User
from src.models.user.entities.enums.user_type import UserType

from src.shared.repositories.sqlalchemy_repository import SQLAlchemyRepository


class SQLAlchemyUsersRepository(SQLAlchemyRepository):
    def __init__(self, client, test=False):
        table_name = "Users"

        if test:
            table_name += "_test"

        table = Table(
            table_name,
            client.mapper_registry.metadata,
            Column("id", Integer, primary_key=True),
            Column("name", String(50)),
            Column("last_name", String(50)),
            Column("address", String(100)),
            Column("email", String(50), unique=True),
            Column("password", String(50)),
            Column("user_type", Enum(UserType)),

            Column("created_at", TIMESTAMP),
            Column("updated_at", TIMESTAMP),
            Column("deleted_at", TIMESTAMP, nullable=True),
        )

        super().__init__(client, User, table, test)
