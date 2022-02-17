from flask import Blueprint, request, make_response
from enviame.inputvalidation import validate_schema_flask
from enviame.inputvalidation import SUCCESS_CODE, FAIL_CODE
from sqlalchemy.exc import IntegrityError
from src.shared.http.crud_blueprint import create_crud_blueprint
from src.models.user.http.validation import user_validatable_fields


def create_users_blueprint(usecase):
    blueprint = Blueprint("users", __name__)

    blueprint = create_crud_blueprint(
        usecase,
        "users",
        user_validatable_fields,
        blueprint
    )

    @blueprint.route("/register", methods=["POST"])
    @validate_schema_flask(user_validatable_fields.CREATION_VALIDATABLE_FIELDS)
    def register():
        body = request.get_json()

        try:
            token = request.cookies.get("access_token")
            entity = usecase.repository.entity_type.from_dict(body)
            data = usecase.register(entity, token)
            code = SUCCESS_CODE
            message = "User created succesfully"
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

        if data is not None and len(data) == 1:
            code = FAIL_CODE
            message = data[0]
            http_code = 400

        response = {
            "code": code,
            "message": message,
        }

        resp = make_response(response, http_code)

        if data is not None and len(data) == 2:
            resp.set_cookie("access_token", data[0])
            resp.set_cookie("refresh_token", data[1])

        return resp

    @blueprint.route("/login", methods=["POST"])
    @validate_schema_flask(user_validatable_fields.SIGN_IN_VALIDATABLE_FIELDS)
    def login():
        body = request.get_json()
        result = usecase.login(body["email"], body["password"])

        if len(result) == 2:
            code = SUCCESS_CODE
            message = "User logged succesfully"
            http_code = 200

        if len(result) == 1:
            code = FAIL_CODE
            message = result[0]
            http_code = 400

        response = {
            "code": code,
            "message": message,
        }

        resp = make_response(response, http_code)

        if len(result) == 2:
            resp.set_cookie("access_token", result[0])
            resp.set_cookie("refresh_token", result[1])

        return resp

    @blueprint.route("/logout", methods=["GET"])
    def logout():
        access_token = request.cookies.get("access_token")
        refresh_token = request.cookies.get("refresh_token")

        if access_token is not None and access_token != "" and refresh_token is not None and refresh_token != "":
            usecase.logout(access_token, refresh_token)
            http_code = 200
            resp = make_response({}, http_code)
            resp.delete_cookie("access_token")
            resp.delete_cookie("refresh_token")
        else:
            http_code = 400
            resp = make_response({}, http_code)

        return resp

    @blueprint.route("/refresh", methods=["GET"])
    def refresh():
        refresh_token = request.cookies.get("refresh_token")

        if refresh_token is not None and refresh_token != "":
            data = usecase.refresh(refresh_token)
            if len(data) == 1:
                return {"message": data[0]}, 400
            http_code = 200
            resp = make_response({}, http_code)
            resp.set_cookie("access_token", data[0])
            resp.set_cookie("refresh_token", data[1])
        else:
            http_code = 400
            resp = make_response({}, http_code)

        return resp

    return blueprint
