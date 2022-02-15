from src.utils.utils import format_date
from src.models.user.entities.enums.user_type import UserType


class User():
    def __init__(
        self,
        id,
        name,
        last_name,
        address,
        email,
        password,
        user_type,
        created_at=None,
        updated_at=None,
        deleted_at=None
    ):
        self.id = id
        self.name = name
        self.last_name = last_name
        self.address = address
        self.email = email
        self.password = password
        self.user_type = user_type

        self.created_at = created_at
        self.updated_at = updated_at
        self.deleted_at = deleted_at

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "last_name": self.last_name,
            "address": self.address,
            "email": self.email,
            "password": self.password,
            "user_type": self.user_type,

            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "deleted_at": self.deleted_at,
        }

    def serialize(self):
        data = self.to_dict()
        data.pop("deleted_at")
        data["created_at"] = format_date(data["created_at"])
        data["updated_at"] = format_date(data["updated_at"])
        data["user_type"] = data["user_type"].name
        return data

    @classmethod
    def from_dict(cls, dict):
        type_values = set(item.name for item in UserType)
        if dict.get("user_type") not in type_values:
            raise ValueError("Invalid User Type")

        id = dict.get("id")
        name = dict.get("name")
        last_name = dict.get("last_name")
        email = dict.get("email")
        address = dict.get("address")
        password = dict.get("password")
        user_type = UserType[dict.get("user_type")]

        created_at = dict.get("created_at")
        updated_at = dict.get("updated_at")
        deleted_at = dict.get("deleted_at")

        return User(
            id,
            name,
            last_name,
            address,
            email,
            password,
            user_type,
            created_at,
            updated_at,
            deleted_at
        )
