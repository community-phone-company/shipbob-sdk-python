from datetime import datetime
from decimal import Decimal
from typing import List, Optional

from pydantic import BaseModel

from .base import Channel
from .inventory import InventoryItemSummary


class FulfillableItemByFulfillmentCenter(BaseModel):
    id: int
    name: str
    fulfillable_quantity: int
    onhand_quantity: int
    committed_quantity: int


class BaseProductModel(BaseModel):
    id: int
    reference_id: Optional[str]
    sku: Optional[str]


class BundleRootInformation(BaseModel):
    id: int
    name: str


class Product(BaseProductModel):
    name: str
    bundle_root_information: Optional[BundleRootInformation]
    created_date: datetime
    channel: Channel
    quantity: Optional[int]
    gtin: Optional[str]
    upc: Optional[str]
    unit_price: Optional[Decimal]
    barcode: Optional[str]

    total_fulfillable_quantity: int
    total_onhand_quantity: int
    total_committed_quantity: int
    fulfillable_inventory_items: List[InventoryItemSummary]
    fulfillable_quantity_by_fulfillment_center: List[FulfillableItemByFulfillmentCenter]


__all__ = ["Product"]
