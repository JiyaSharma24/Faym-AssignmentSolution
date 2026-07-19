from enum import Enum


class SaleStatus(Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


class PayoutType(Enum):
    ADVANCE = "advance"
    FINAL = "final"


class PayoutStatus(Enum):
    PENDING = "pending"
    SUCCESS = "success"
    FAILED = "failed"
    CANCELLED = "cancelled"
    REJECTED = "rejected"