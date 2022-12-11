from datetime import datetime
from decimal import Decimal
from typing import Any, List, Optional

from pydantic import BaseModel


class InventoryItemDimensions(BaseModel):
    weight: Decimal
    length: Decimal
    width: Decimal
    depth: Decimal


class FulfillableQuantityByFulfillmentCenter(BaseModel):
    id: int
    name: str
    fulfillable_quantity: int
    onhand_quantity: int
    committed_quantity: int
    awaiting_quantity: int
    internal_transfer_quantity: int


class FulfillableQuantityByLot(BaseModel):
    lot_number: Optional[int]
    expiration_date: Optional[datetime]
    fulfillable_quantity: int
    onhand_quantity: int
    committed_quantity: int
    awaiting_quantity: int
    internal_transfer_quantity: int
    fulfillable_quantity_by_fulfillment_center: List[FulfillableQuantityByFulfillmentCenter]


class InventoryItem(BaseModel):
    id: int
    name: str
    is_digital: bool
    is_case_pick: bool
    is_lot: bool
    dimensions: InventoryItemDimensions
    total_fulfillable_quantity: int
    total_onhand_quantity: int
    total_committed_quantity: int
    total_sellable_quantity: int
    total_awaiting_quantity: int
    total_exception_quantity: int
    total_internal_transfer_quantity: int
    total_backordered_quantity: int
    is_active: bool
    fulfillable_quantity_by_fulfillment_center: List[FulfillableQuantityByFulfillmentCenter]
    fulfillable_quantity_by_lot: List[FulfillableQuantityByLot]
    packaging_attribute: Optional[Any]


class InventoryItemSummary(BaseModel):
    id: int
    name: str
    quantity: int


__all__ = ["InventoryItem", "InventoryItemSummary"]
