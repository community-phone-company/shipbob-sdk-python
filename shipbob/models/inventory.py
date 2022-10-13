from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class InventoryItem(BaseModel):
    id: int
    name: str
    quantity: int
    quantity_committed: int
    lot: Optional[str]
    expiration_date: Optional[datetime]
    serial_numbers: List[str]
    is_dangerous_goods: bool


class InventoryItemSummary(BaseModel):
    id: int
    name: str
    quantity: int


class FullfillableItemByFulfillmentCenter(BaseModel):
    id: int
    name: str
    fulfillable_quantity: int
    onhand_quantity: int
    committed_quantity: int


__all__ = ["InventoryItem", "InventoryItemSummary"]
