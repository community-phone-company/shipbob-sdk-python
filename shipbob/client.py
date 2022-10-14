import logging
import os
from typing import Iterator, List

from requests import Session

from .models.orders import Order
from .models.products import Product
from .models.shipping import Shipment

logger = logging.getLogger(__name__)


class ShipBob(Session):
    BASE_URL = "https://api.shipbob.com/1.0"

    ACCESS_TOKEN = os.getenv("SHIPBOB_ACCESS_TOKEN")

    MAX_PAGE_SIZE: int = 250

    def __init__(self):
        super().__init__()
        if not self.ACCESS_TOKEN:
            raise ValueError("Please set SHIPBOB_ACCESS_TOKEN environment variable")

        self.headers.update(
            {"Content-Type": "application/json", "Authorization": f"Bearer {self.ACCESS_TOKEN}"}
        )

    def request(self, method, url, *args, **kwargs):
        url = "/".join((self.BASE_URL, url.lstrip("/")))
        return super().request(method, url, *args, **kwargs)

    def get_orders(self, **params) -> List[Order]:
        response = self.request("GET", "order", params=params)
        response.raise_for_status()
        return [Order(**order_data) for order_data in response.json()]

    def get_order_shipments(self, order, **params) -> List[Shipment]:
        response = self.request("GET", f"order/{order.id}/shipment", params=params)
        response.raise_for_status()
        return [Shipment(**shipment_data) for shipment_data in response.json()]

    def get_products(self, **params) -> List[Product]:
        response = self.request("GET", "product", params=params)
        response.raise_for_status()
        return [Product(**product_data) for product_data in response.json()]

    def iterate_products(self, **params) -> Iterator[Product]:
        params.pop("page", None)
        params.pop("limit", None)
        params["SortOrder"] = "Oldest"

        page = 1
        while products := self.get_products(page=page, limit=self.MAX_PAGE_SIZE, **params):
            logger.debug(f"Getting page {page} of products")
            for product in products:
                yield product
            page += 1

    def iterate_orders(self, **params) -> Iterator[Order]:
        params.pop("page", None)
        params.pop("limit", None)

        page = 1
        while orders := self.get_orders(page=page, limit=self.MAX_PAGE_SIZE, **params):
            logger.debug(f"Getting page {page} of orders")
            for order in orders:
                yield order
            page += 1
