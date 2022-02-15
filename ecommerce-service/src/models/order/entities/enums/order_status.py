from enum import Enum

class OrderStatus(Enum):
    CREATED = 0
    CONFIRMED = 1
    DISPACHED = 2
    DELIVERED = 3