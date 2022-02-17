from src.shared.usecases.crud_usecase import CrudUsecase


class ManageSellersUsecase(CrudUsecase):
    def __init__(self, repository):
        super().__init__(repository)

    def find_by_user(self, id):
        return self.repository.find_by_user(id)