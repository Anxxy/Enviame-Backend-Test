from src.shared.http.crud_blueprint import create_crud_blueprint
from src.models.seller.http.validation import seller_validatable_fields


def create_sellers_blueprint(usecase):
    blueprint = create_crud_blueprint(
        usecase,
        "sellers",
        seller_validatable_fields
    )
    return blueprint
