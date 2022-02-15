class SQLAlchemyRepository():
    def __init__(self, sqlalchemy_client, entity_type, table, test=False):
        self.client = sqlalchemy_client
        self.session_factory = sqlalchemy_client.session_factory
        self.table = table
        self.entity_type = entity_type
        self.test = test

        sqlalchemy_client.mapper_registry.map_imperatively(
            entity_type,
            self.table
        )

    def find_all(self):
        with self.session_factory() as session:
            results = session.query(self.entity_type).filter_by(
                deleted_at=None).all()
            return results

    def find_by_id(self, id):
        with self.session_factory() as session:
            results = session.query(self.entity_type).filter_by(
                id=id,
                deleted_at=None
            ).first()
            return results

    def create(self, entity):
        with self.session_factory() as session:
            session.add(entity)
            session.commit()
            return entity

    def update(self, id, fields):
        with self.session_factory() as session:
            session.query(self.entity_type).filter_by(
                id=id, deleted_at=None).update(fields)
            session.commit()

            result = session.query(self.entity_type).filter_by(
                id=id, deleted_at=None).first()
            return result

    def delete(self, id):
        with self.session_factory() as session:
            result = session.query(self.entity_type).get(id)
            session.delete(result)
            session.commit()

    def delete_all(self):
        if self.test:
            with self.session_factory() as session:
                session.query(self.entity_type).delete()
                session.commit()

    def drop_table(self):
        if self.test:
            self.client.drop_table(self.table)
