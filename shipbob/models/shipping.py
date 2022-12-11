from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Dict, List, Optional

from pydantic import BaseModel

from .base import Address, BaseMeasurementModel
from .products import BaseProductModel


class CarrierType(Enum):
    PARCEL = "Parcel"
    FREIGHT = "Freight"


class PaymentTermType(Enum):
    COLLECT = "Collect"
    THIRD_PARTY = "ThirdParty"
    PREPAID = "Prepaid"
    MERCHANT_RESPONSIBLE = "MerchantResponsible"


class ShipmentStatus(Enum):
    NONE = None
    PROCESSING = "Processing"
    PENDING = "Pending"
    COMPLETED = "Completed"
    EXCEPTION = "Exception"
    HELD = "OnHold"
    CANCELLED = "Cancelled"
    CLEAN_SWEEPED = "CleanSweeped"
    LABELED = "LabeledCreated"
    IMPORT_REVIEW = "ImportReview"


class PackageMaterialType(Enum):
    UNKNOWN = "Unknown"
    BOX = "Box"
    BUBBLE_MAILER = "BubbleMailer"
    POLYMAILER = "PolyMailer"
    FRAGILE_BOX = "FragileBox"
    POSTER_TUBE = "PosterTube"
    CUSTOM = "Custom"
    BOOKFOLD = "Bookfold"
    OWN_CONTAINER = "OwnContainer"
    UNDEFINED = "Undefined"


class EstimatedFulfillmentStatus(Enum):
    AWAITING_INVENTORY_ALLOCATION = "AwaitingInventoryAllocation"
    AWAITING_RESET = "AwaitingReset"
    UNAVAILABLE = "Unavailable"
    PENDING_ON_TIME = "PendingOnTime"
    FULFILLED_ON_TIME = "FulfilledOnTime"
    PENDING_LATE = "PendingLate"
    FULFILLED_LATE = "FulfilledLate"


class CartonBaseModel(BaseModel):
    type: str
    barcode: str
    measurements: BaseMeasurementModel


class Recipient(BaseModel):
    name: str
    address: Address
    email: Optional[str]
    phone_number: Optional[str]


class ShipmentStatusDetail(BaseModel):
    name: str
    description: str
    id: int
    inventory_id: Optional[int]
    exception_fullfilment_center_id: Optional[int]


class TrackingDetail(BaseModel):
    carrier: str
    tracking_number: str
    carrier_service: Optional[str]
    tracking_url: Optional[str]
    bol: Optional[str]
    shipping_date: Optional[datetime]
    pro_number: Optional[str]
    scac: Optional[str]


class ShippedInventoryItem(BaseModel):
    id: int
    name: str
    quantity: int
    quantity_committed: int
    lot: Optional[str]
    expiration_date: Optional[datetime]
    serial_numbers: List[str]
    is_dangerous_goods: bool


class ShippedProduct(BaseProductModel):
    name: str
    inventory_items: List[ShippedInventoryItem]


class Carton(CartonBaseModel):
    carton_details: List[ShippedProduct]


class ParentCarton(CartonBaseModel):
    cartons: List[Carton]


class FulfillmentCenter(BaseModel):
    id: int
    name: str


class Shipment(BaseModel):
    id: int
    store_order_id: Optional[str]
    order_id: int
    reference_id: Optional[str]
    created_date: datetime
    last_update_at: Optional[datetime]
    status: ShipmentStatus
    status_detail: Optional[ShipmentStatusDetail]
    location: Optional[FulfillmentCenter]
    invoice_amount: Decimal
    insurance_value: Optional[Decimal]
    ship_option: str
    package_material_type: PackageMaterialType
    tracking: Optional[TrackingDetail]
    products: List[ShippedProduct]
    parent_cartons: List[ParentCarton]
    measurements: Optional[BaseMeasurementModel]
    require_signature: bool
    estimated_fulfillment_date: Optional[datetime]
    estimated_fulfillment_date_status: EstimatedFulfillmentStatus
    actual_fulfllment_date: Optional[datetime]
    is_tracking_uploaded: bool
    gift_message: Optional[str]


class ShippingTerms(BaseModel):
    carrier_type: Optional[CarrierType]
    payment_term: Optional[PaymentTermType]


class ShipmentEvent(BaseModel):
    log_type_id: int
    log_type_name: str
    log_type_text: str
    timestamp: datetime
    metadata: Optional[Dict]


__all__ = [
    "CarrierType",
    "PaymentTermType",
    "ShipmentStatus",
    "PackageMaterialType",
    "EstimatedFulfillmentStatus",
    "FulfillmentCenter",
    "Recipient",
    "ShipmentStatusDetail",
    "TrackingDetail",
    "ShippedInventoryItem",
    "ShippedProduct",
    "Carton",
    "ParentCarton",
    "Shipment",
    "ShippingTerms",
    "ShipmentEvent",
]
