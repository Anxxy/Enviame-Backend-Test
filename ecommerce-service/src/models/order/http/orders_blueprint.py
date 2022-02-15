from src.shared.http.crud_blueprint import create_crud_blueprint
from src.models.order.http.validation import order_validatable_fields


def create_orders_blueprint(usecase):
    blueprint = create_crud_blueprint(
        usecase,
        "orders",
        order_validatable_fields
    )
    return blueprint
