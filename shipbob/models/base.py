from decimal import Decimal
from enum import Enum
from typing import Optional

from pydantic import BaseModel


class RetailerProgramDataType(Enum):
    MARK_FOR = "MarkFor"
    SHIP_FROM = "ShipFrom"


class Channel(BaseModel):
    id: int
    name: str


class Address(BaseModel):
    address1: Optional[str]
    address2: Optional[str]
    city: Optional[str]
    state: Optional[str]
    country: Optional[str]
    zip_code: Optional[str]


class RetailerProgramData(Address):
    type: Optional[RetailerProgramDataType]
    company_name: Optional[str]


class BaseMeasurementModel(BaseModel):
    total_weight_oz: Decimal
    length_in: Decimal
    width_in: Decimal
    depth_in: Decimal


class Tag(BaseModel):
    name: str
    value: str
