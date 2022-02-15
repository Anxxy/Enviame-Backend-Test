CREATION_VALIDATABLE_FIELDS = {
    "name": {
        "required": True,
        "type": "string",
    },
    "last_name": {
        "required": True,
        "type": "string",
    },
    "email": {
        "required": True,
        "type": "string",
    },
    "address": {
        "required": True,
        "type": "string",
    },
    "password": {
        "required": True,
        "type": "string",
    },
    "user_type": {
        "required": True,
        "type": "string"
    }
}

UPDATE_VALIDATABLE_FIELDS = {
    "name": {
        "required": False,
        "type": "string",
    },
    "last_name": {
        "required": False,
        "type": "string",
    },
    "email": {
        "required": False,
        "type": "string",
    },
    "address": {
        "required": False,
        "type": "string",
    },
    "password": {
        "required": False,
        "type": "string",
    },
    "user_type": {
        "required": False,
        "type": "string"
    }
}
