CREATION_VALIDATABLE_FIELDS = {
    "quantity": {
        "required": True,
        "type": "integer",
    },
    "buyer": {
        "required": True,
        "type": "integer",
    },
    "seller": {
        "required": True,
        "type": "integer",
    },
}

UPDATE_VALIDATABLE_FIELDS = {
    "quantity": {
        "required": False,
        "type": "integer",
    },
    "buyer": {
        "required": False,
        "type": "integer",
    },
    "seller": {
        "required": False,
        "type": "integer",
    },
}
