from src.shared.http.crud_blueprint import create_crud_blueprint
from src.models.product.http.validation import product_validatable_fields


def create_products_blueprint(usecase):
    blueprint = create_crud_blueprint(
        usecase,
        "products",
        product_validatable_fields
    )
    return blueprint
