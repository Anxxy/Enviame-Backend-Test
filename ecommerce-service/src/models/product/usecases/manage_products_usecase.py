from src.shared.usecases.crud_usecase import CrudUsecase


class ManageProductsUsecase(CrudUsecase):
    def __init__(self, repository):
        super().__init__(repository)
