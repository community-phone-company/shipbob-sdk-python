import logging
import os
import time
from datetime import datetime, timedelta
from typing import Iterator, List

from pydantic import ValidationError
from requests import Session

from .models.orders import Order
from .models.products import Product
from .models.shipping import Shipment, ShipmentEvent

logger = logging.getLogger(__name__)


class ShipBobClient(Session):
    BASE_URL = "https://api.shipbob.com/1.0"

    ACCESS_TOKEN = os.getenv("SHIPBOB_ACCESS_TOKEN")

    MAX_PAGE_SIZE: int = 250
    MAX_REQUESTS_PER_MINUTE: int = 150  # As per ShipBob docs, 150 reqs/min sliding window

    def __init__(self):
        super().__init__()
        if not self.ACCESS_TOKEN:
            raise ValueError("Please set SHIPBOB_ACCESS_TOKEN environment variable")

        self.headers.update(
            {"Content-Type": "application/json", "Authorization": f"Bearer {self.ACCESS_TOKEN}"}
        )

        self._request_window = []

    def _clear_request_window(self):
        now = datetime.now()
        one_minute_old = now - timedelta(seconds=60)
        self._request_window = [rt for rt in self._request_window if rt >= one_minute_old]

    def request(self, method, url, *args, **kwargs):
        while len(self._request_window) >= self.MAX_REQUESTS_PER_MINUTE:
            logger.info("Hitting rate limit. Sleeping for one second")
            self._clear_request_window()
            time.sleep(1)

        self._request_window.append(datetime.now())

        url = "/".join((self.BASE_URL, url.lstrip("/")))
        response = super().request(method, url, *args, **kwargs)
        response.raise_for_status()
        return response

    def get_orders(self, **params) -> List[Order]:
        response = self.request("GET", "order", params=params)
        response.raise_for_status()
        return [Order(**order_data) for order_data in response.json()]

    def get_order_shipments(self, order, **params) -> List[Shipment]:
        response = self.request("GET", f"order/{order.id}/shipment", params=params)
        response.raise_for_status()
        return [Shipment(**shipment_data) for shipment_data in response.json()]

    def get_shipment_events(self, shipment, **params) -> List[ShipmentEvent]:
        try:
            response = self.request("GET", f"shipment/{shipment.id}/timeline", params=params)
            response.raise_for_status()
            return [ShipmentEvent(**timeline) for timeline in response.json()]
        except ValidationError as exc:
            logger.warn(f"Failed to get events for {shipment}: {exc}")
            return []

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
