from dataclasses import fields
from flask import request
from src.shared.http.crud_blueprint import create_crud_blueprint
from src.models.seller.http.validation import seller_validatable_fields
from src.models.user.entities.enums.user_type import UserType
from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError
from enviame.inputvalidation import validate_schema_flask
from enviame.inputvalidation import SUCCESS_CODE, FAIL_CODE
from sqlalchemy.exc import IntegrityError
from src.utils import utils
from src.utils import globals


def create_sellers_blueprint(usecase):
    def permissions_verifier(request_type):
        access_token = request.cookies.get("access_token")

        if access_token is None or access_token == "":
            return False

        try:
            user_info = utils.decode_access_token(globals.SECRET, access_token)
        except (ExpiredSignatureError, InvalidSignatureError):
            return False

        if UserType[user_info["type"]] == UserType.ADMINISTRATOR:
            return True

        # if request_type in ["read", "update"]:
        #     if UserType[user_info["type"]] == UserType.SELLER:
        #         return True

        return False

    blueprint = create_crud_blueprint(
        usecase,
        "sellers",
        seller_validatable_fields,
        filters=[permissions_verifier]
    )

    @blueprint.route("/seller", methods=["PUT"])
    @validate_schema_flask(seller_validatable_fields.UPDATE_VALIDATABLE_FIELDS)
    def update_seller():
        body = request.get_json()
        # fields = usecase.repository.entity_type.from_dict(body)

        access_token = request.cookies.get("access_token")

        if access_token is None or access_token == "":
            return {
                "message": "Missing Access Token",
                "code": FAIL_CODE
            }, 400

        try:
            user_info = utils.decode_access_token(globals.SECRET, access_token)
        except (ExpiredSignatureError, InvalidSignatureError):
            return {
                "message": "Invalid Access Token",
                "code": FAIL_CODE
            }, 400

        if UserType[user_info["type"]] != UserType.SELLER:
            return {
                "message": "User is not an Seller",
                "code": FAIL_CODE
            }, 400
        
        try:
            entity = usecase.find_by_user(user_info["user_id"])
            data = usecase.update(entity.id, body).serialize()
            message = "Seller updated succesfully"
            code = SUCCESS_CODE
            http_code = 200
        except ValueError as e:
            data = None
            code = FAIL_CODE
            message = str(e)
            http_code = 400
        except IntegrityError as e:
            data = None
            code = FAIL_CODE
            message = e.orig.args[1]
            http_code = 400
            
        response = {
            "code": code,
            "message": message,
        }

        if data:
            response["data"] = data

        return response, http_code

    return blueprint
