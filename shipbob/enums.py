from enum import Enum


class CarrierType(Enum):
    PARCEL = "Parcel"
    FREIGHT = "Freight"


class PaymentTermType(Enum):
    COLLECT = "Collect"
    THIRD_PARTY = "ThirdParty"
    PREPAID = "Prepaid"
    MERCHANT_RESPONSIBLE = "MerchantResponsible"


class OrderStatus(Enum):
    PROCESSING = "Processing"
    EXCEPTION = "Exception"
    PARTIALLY_FULFILLED = "PartiallyFulfilled"
    FULFILLED = "Fulfilled"
    CANCELLED = "Cancelled"
    IMPORT_REVIEW = "ImportReview"


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


class OrderType(Enum):
    DTC = "DTC"
    DROPSHIP = "DropShip"
    B2B = "B2B"


class RetailerProgramDataType(Enum):
    MARK_FOR = "MarkFor"
    SHIP_FROM = "ShipFrom"


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
