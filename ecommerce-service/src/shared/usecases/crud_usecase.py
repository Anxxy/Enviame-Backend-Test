from src.utils import utils


class CrudUsecase():
    def __init__(self, repository):
        self.repository = repository

    def find_all(self):
        return self.repository.find_all()

    def find_by_id(self, id):
        return self.repository.find_by_id(id)

    def create(self, entity):
        current_time = utils.get_current_datetime()

        if hasattr(entity, 'created_at'):
            entity.created_at = current_time

        if hasattr(entity, 'updated_at'):
            entity.updated_at = current_time

        return self.repository.create(entity)

    def update(self, id, fields):
        entity = self.repository.find_by_id(id)
        current_time = utils.get_current_datetime()

        if entity:
            if hasattr(fields, 'updated_at'):
                fields.updated_at = current_time

            return self.repository.update(id, fields)
        else:
            raise ValueError(
                f"{self.repository.table.name} of ID {id} doesn't exist.")

    def delete(self, id):
        entity = self.repository.find_by_id(id)
        current_time = utils.get_current_datetime()

        if entity:
            data = {
                "deleted_at": current_time
            }

            self.repository.update(id, data)
        else:
            raise ValueError(
                f"{self.repository.table.name} of ID {id} doesn't exist or is already deleted.")
