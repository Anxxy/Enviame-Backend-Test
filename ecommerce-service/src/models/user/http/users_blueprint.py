from src.shared.http.crud_blueprint import create_crud_blueprint
from src.models.user.http.validation import user_validatable_fields


def create_users_blueprint(usecase):
    blueprint = create_crud_blueprint(
        usecase,
        "users",
        user_validatable_fields
    )
    return blueprint
