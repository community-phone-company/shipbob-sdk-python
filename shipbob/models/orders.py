from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel

from .base import Channel, RetailerProgramData, Tag
from .products import BaseProductModel
from .shipping import Recipient, Shipment, ShippingTerms


class OrderStatus(Enum):
    PROCESSING = "Processing"
    EXCEPTION = "Exception"
    PARTIALLY_FULFILLED = "PartiallyFulfilled"
    FULFILLED = "Fulfilled"
    CANCELLED = "Cancelled"
    IMPORT_REVIEW = "ImportReview"


class OrderType(Enum):
    DTC = "DTC"
    DROPSHIP = "DropShip"
    B2B = "B2B"


class OrderedProduct(BaseProductModel):
    quantity: int
    quantity_unit_of_measure_code: str
    gtin: str
    upc: str
    unit_price: Decimal
    external_line_id: int


class Order(BaseModel):
    id: int
    created_date: datetime
    purchase_date: Optional[datetime]
    reference_id: Optional[str]
    order_number: Optional[str]
    status: OrderStatus
    type: OrderType
    channel: Optional[Channel]
    shipping_method: Optional[str]
    recipient: Optional[Recipient]
    products: List[OrderedProduct]
    tags: List[Tag]
    shipments: List[Shipment]
    gift_message: Optional[str]
    shipping_terms: ShippingTerms
    retailer_program_data: RetailerProgramData


__all__ = ["Order", "OrderStatus", "OrderType"]
