from src.models.order.entities.enums.order_status import OrderStatus
from src.utils.utils import format_date


class Order():
    def __init__(
        self,
        id,
        buyer,
        seller,
        quantity,
        status,
        created_at=None,
        updated_at=None,
        deleted_at=None
    ):
        self.id = id
        self.buyer = buyer
        self.seller = seller
        self.quantity = quantity
        self.status = status

        self.created_at = created_at
        self.updated_at = updated_at
        self.deleted_at = deleted_at

    def to_dict(self):
        return {
            "id": self.id,
            "buyer": self.buyer,
            "seller": self.seller,
            "quantity": self.quantity,
            "status": self.status,

            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "deleted_at": self.deleted_at,
        }

    def serialize(self):
        data = self.to_dict()
        data.pop("deleted_at")
        data["created_at"] = format_date(data["created_at"])
        data["updated_at"] = format_date(data["updated_at"])
        data["status"] = data["status"].name
        return data

    @classmethod
    def from_dict(cls, dict):
        type_values = set(item.name for item in OrderStatus)
        if dict.get("status") not in type_values:
            raise ValueError("Invalid Order Status")
        
        id = dict.get("id")
        seller = dict.get("seller")
        buyer = dict.get("buyer")
        quantity = dict.get("quantity")
        status = OrderStatus[dict.get("status")]

        created_at = dict.get("created_at")
        updated_at = dict.get("updated_at")
        deleted_at = dict.get("deleted_at")

        return Order(
            id,
            buyer,
            seller,
            quantity,
            status,
            created_at,
            updated_at,
            deleted_at
        )
