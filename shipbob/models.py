from datetime import datetime
from decimal import Decimal
from typing import List, Optional

from pydantic import BaseModel

from . import enums


class BaseProductModel(BaseModel):
    id: int
    reference_id: Optional[str]
    sku: Optional[str]


class BaseMeasurementModel(BaseModel):
    total_weight_oz: Decimal
    length_in: Decimal
    width_in: Decimal
    depth_in: Decimal


class Address(BaseModel):
    address1: Optional[str]
    address2: Optional[str]
    city: Optional[str]
    state: Optional[str]
    country: Optional[str]
    zip_code: Optional[str]


class Channel(BaseModel):
    id: int
    name: str


class CartonBaseModel(BaseModel):
    type: str
    barcode: str
    measurements: BaseMeasurementModel


class FulfillmentCenter(BaseModel):
    id: int
    name: str


class InventoryItem(BaseModel):
    id: int
    name: str
    quantity: int
    quantity_committed: int
    lot: Optional[str]
    expiration_date: Optional[datetime]
    serial_numbers: List[str]
    is_dangerous_goods: bool


class Product(BaseProductModel):
    reference_id: Optional[str]
    quantity: int
    quantity_unit_of_measure_code: str
    gtin: str
    upc: str
    unit_price: Decimal
    external_line_id: int


class Recipient(BaseModel):
    name: str
    address: Address
    email: Optional[str]
    phone_number: Optional[str]


class RetailerProgramData(Address):
    type: Optional[enums.RetailerProgramDataType]
    company_name: Optional[str]


class ShipmentStatusDetail(BaseModel):
    name: str
    description: str
    id: int
    inventory_id: Optional[int]
    exception_fullfilment_center_id: Optional[int]


class TrackingDetail(BaseModel):
    carrier: str
    tracking_number: str
    carrier_service: str
    tracking_url: str
    bol: Optional[str]
    shipping_date: Optional[datetime]
    pro_number: Optional[str]
    scac: Optional[str]


class ShippedProduct(BaseProductModel):
    name: str
    inventory_items: List[InventoryItem]


class Carton(CartonBaseModel):
    carton_details: List[ShippedProduct]


class ParentCarton(CartonBaseModel):
    cartons: List[Carton]


class Shipment(BaseModel):
    id: int
    store_order_id: Optional[str]
    order_id: int
    reference_id: Optional[str]
    created_date: datetime
    last_update_at: Optional[datetime]
    status: enums.ShipmentStatus
    status_detail: Optional[ShipmentStatusDetail]
    location: FulfillmentCenter
    invoice_amount: Decimal
    insurance_value: Optional[Decimal]
    ship_option: str
    package_material_type: enums.PackageMaterialType
    tracking: Optional[TrackingDetail]
    products: List[ShippedProduct]
    parent_cartons: List[ParentCarton]
    measurements: BaseMeasurementModel
    require_signature: bool
    estimated_fulfillment_date: Optional[datetime]
    estimated_fulfillment_date_status: enums.EstimatedFulfillmentStatus
    actual_fulfllment_date: Optional[datetime]
    is_tracking_uploaded: bool
    gift_message: Optional[str]


class ShippingTerms(BaseModel):
    carrier_type: Optional[enums.CarrierType]
    payment_term: Optional[enums.PaymentTermType]


class Tag(BaseModel):
    name: str
    value: str


class Order(BaseModel):
    id: int
    created_date: datetime
    purchase_date: Optional[datetime]
    reference_id: Optional[str]
    order_number: Optional[str]
    status: enums.OrderStatus
    type: enums.OrderType
    channel: Channel
    shipping_method: Optional[str]
    recipient: Optional[Recipient]
    products: List[Product]
    tags: List[Tag]
    shipments: List[Shipment]
    gift_message: Optional[str]
    shipping_terms: ShippingTerms
    retailer_program_data: RetailerProgramData
