from src.shared.usecases.crud_usecase import CrudUsecase


class ManageOrdersUsecase(CrudUsecase):
    def __init__(self, repository):
        super().__init__(repository)
