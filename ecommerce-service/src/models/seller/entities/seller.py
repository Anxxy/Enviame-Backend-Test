from src.utils.utils import format_date


class Seller():
    def __init__(self, id, name, description, address, user, created_at=None, updated_at=None, deleted_at=None):
        self.id = id
        self.name = name
        self.description = description
        self.address = address
        self.user = user

        self.created_at = created_at
        self.updated_at = updated_at
        self.deleted_at = deleted_at

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "address": self.address,
            "user": self.user,
            
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "deleted_at": self.deleted_at,
        }
    
    def serialize(self):
        data = self.to_dict()
        data.pop("deleted_at")
        data["created_at"] = format_date(data["created_at"])
        data["updated_at"] = format_date(data["updated_at"])
        return data
    
    @classmethod
    def from_dict(cls, dict):
        id = dict.get("id")
        name = dict.get("name")
        description = dict.get("description")
        address = dict.get("address")
        user = dict.get("user")
        
        created_at = dict.get("created_at")
        updated_at = dict.get("updated_at")
        deleted_at = dict.get("deleted_at")
        
        return Seller(id, name, description, address, user, created_at, updated_at, deleted_at)