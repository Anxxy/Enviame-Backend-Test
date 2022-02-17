from flask import Blueprint, request
from src.shared.http.crud_blueprint import create_crud_blueprint
from src.models.product.http.validation import product_validatable_fields
from src.models.user.entities.enums.user_type import UserType
from enviame.inputvalidation import SUCCESS_CODE, FAIL_CODE
from enviame.inputvalidation import validate_schema_flask
from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError
from src.utils import utils
from src.utils import globals


def create_products_blueprint(usecase):
    blueprint = Blueprint("products", __name__)

    # blueprint = create_crud_blueprint(
    #     usecase,
    #     "products",
    #     product_validatable_fields,
    #     blueprint,
    # )

    @blueprint.route("/products", methods=["GET"])
    def find_products():
        access_token = request.cookies.get("access_token")
        if access_token is None or access_token == "":
            return {
                "message": "Missing Access Token",
                "code": FAIL_CODE
            }, 400
        try:
            user_info = utils.decode_access_token(globals.SECRET, access_token)
        except (ExpiredSignatureError, InvalidSignatureError) as e:
            return {
                "message": str(e),
                "code": FAIL_CODE
            }, 400

        data = None
        code = SUCCESS_CODE
        http_code = 200
        message = ""

        if UserType[user_info["type"]] == UserType.ADMINISTRATOR:
            data = usecase.find_all()

        if UserType[user_info["type"]] == UserType.SELLER:
            data = usecase.find_seller_products(user_info["user_id"])

        if data is not None:
            res = []
            for i in data:
                res.append(i.serialize())
            data = res

        if UserType[user_info["type"]] == UserType.MARKETPLACE:
            data = usecase.find_all_products_with_seller()

        response = {
            "data": data,
            "code": code,
            "message": message,
        }

        return response, http_code

    @blueprint.route("/products", methods=["POST"])
    @validate_schema_flask(product_validatable_fields.CREATION_VALIDATABLE_FIELDS)
    def create_products():
        body = request.get_json()
        pass

    return blueprint
