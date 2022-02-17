from sqlalchemy import Table, Column, String
from src.models.refresh_token.entities.refresh_token import RefreshToken
from src.shared.repositories.sqlalchemy_repository import SQLAlchemyRepository


class SQLAlchemyRefreshTokenRepository(SQLAlchemyRepository):
    def __init__(self, client, test=False):
        table_name = "RefreshToken"

        if test:
            table_name += "_test"

        table = Table(
            table_name,
            client.mapper_registry.metadata,
            Column("id", String(50), primary_key=True),
            Column("token", String(50), unique=True),
        )

        super().__init__(client, RefreshToken, table, test)

    def find_by_id(self, id):
        with self.session_factory() as session:
            results = session.query(self.entity_type).filter_by(
                id=id,
            ).first()
            return results

    def find_by_token(self, token):
        with self.session_factory() as session:
            results = session.query(self.entity_type).filter_by(
                token=token,
            ).first()
            return results
