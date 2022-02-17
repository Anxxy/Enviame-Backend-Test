from src.shared.usecases.crud_usecase import CrudUsecase


class ManageProductsUsecase(CrudUsecase):
    def __init__(self, repository, seller_repository):
        super().__init__(repository)
        self.seller_repository = seller_repository

    def find_seller_products(self, seller_id):
        seller = self.seller_repository.find_by_user(seller_id)
        products = self.repository.find_by_seller(seller.id)
        return products

    def find_all_products_with_seller(self):
        result = []
        sellers = self.seller_repository.find_all()
        for seller in sellers:
            products_list = []
            products = self.repository.find_by_seller(seller.id)
            for product in products:
                products_list.append(product.serialize())

            result.append({
                "seller": seller.serialize(),
                "products": products_list
            })

        return result
