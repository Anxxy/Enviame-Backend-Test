CREATION_VALIDATABLE_FIELDS = {
    "name": {
        "required": True,
        "type": "string",
    },
    "description": {
        "required": True,
        "type": "string",
    },
    "address": {
        "required": True,
        "type": "string",
    },
    "user": {
        "required": True,
        "type": "integer",
    },
}

UPDATE_VALIDATABLE_FIELDS = {
    "name": {
        "required": False,
        "type": "string",
    },
    "description": {
        "required": False,
        "type": "string",
    },
    "address": {
        "required": False,
        "type": "string",
    },
    "user": {
        "required": False,
        "type": "integer",
    },
}