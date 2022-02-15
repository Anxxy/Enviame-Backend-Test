from flask import Blueprint, request
from enviame.inputvalidation import validate_schema_flask
from enviame.inputvalidation import SUCCESS_CODE, FAIL_CODE
from sqlalchemy.exc import IntegrityError


def create_crud_blueprint(usecase, title, validatable_fields, blueprint=None):
    if blueprint is None:
        blueprint = Blueprint(title, __name__)

    @blueprint.route(f"/{title}", methods=["GET"])
    def find_all():
        entities = usecase.find_all()

        entities_dict = []
        for entity in entities:
            entities_dict.append(entity.serialize())

        data = entities_dict
        code = SUCCESS_CODE
        message = f"{title.capitalize()} obtained succesfully"
        http_code = 200

        response = {
            "code": code,
            "message": message,
            "data": data,
        }

        return response, http_code

    @blueprint.route(f"/{title}/<string:id>", methods=["GET"])
    def find_by_id(id):
        entity = usecase.find_by_id(id)

        if entity:
            data = entity.serialize()
            code = SUCCESS_CODE
            message = f"{title.capitalize()} obtained succesfully"
            http_code = 200

        else:
            data = None
            code = FAIL_CODE
            message = f"{title.capitalize()} of ID {id} does not exist."
            http_code = 404

        response = {
            "code": code,
            "message": message,
        }

        if data:
            response["data"] = data

        return response, http_code

    @blueprint.route(f"/{title}", methods=["POST"])
    @validate_schema_flask(validatable_fields.CREATION_VALIDATABLE_FIELDS)
    def create():
        body = request.get_json()

        try:
            entity = usecase.repository.entity_type.from_dict(body)
            entity = usecase.create(entity)
            data = entity.serialize()
            code = SUCCESS_CODE
            message = f"{title.capitalize()} created succesfully"
            http_code = 201

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

    @blueprint.route(f"/{title}/<string:id>", methods=["PUT"])
    @validate_schema_flask(validatable_fields.UPDATE_VALIDATABLE_FIELDS)
    def update(id):
        body = request.get_json()
        entity = usecase.repository.entity_type.from_dict(body)

        try:
            entity = usecase.update(id, entity)
            data = entity.serialize()
            message = f"{title.capitalize()} updated succesfully"
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

    @blueprint.route(f"/{title}/<string:id>", methods=["DELETE"])
    def delete(id):
        try:
            usecase.delete(id)
            code = SUCCESS_CODE
            message = f"{title.capitalize()} of ID {id} deleted succesfully."
            http_code = 200

        except ValueError as e:
            code = FAIL_CODE
            message = str(e)
            http_code = 400

        response = {
            "code": code,
            "message": message,
        }

        return response, http_code

    return blueprint
