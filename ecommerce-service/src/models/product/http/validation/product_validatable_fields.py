CREATION_VALIDATABLE_FIELDS = {
    "name": {
        "required": True,
        "type": "string",
    },
    "description": {
        "required": True,
        "type": "string",
    },
    "quantity": {
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
    "quantity": {
        "required": False,
        "type": "integer",
    },
}
