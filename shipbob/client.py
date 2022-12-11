import logging
import os
import time
from datetime import datetime, timedelta
from typing import Iterator, List

from pydantic import ValidationError
from requests import Session
from requests.exceptions import HTTPError

from .models.inventory import InventoryItem
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

        self._request_bucket = []

    def _clear_request_bucket(self):
        now = datetime.now()
        one_minute_old = now - timedelta(seconds=60)
        self._request_bucket = [rt for rt in self._request_bucket if rt >= one_minute_old]

    def request(self, method, url, retry_on_rate_limit=True, *args, **kwargs):
        while len(self._request_bucket) >= self.MAX_REQUESTS_PER_MINUTE:
            logger.warning("Close to rate limit. Sleeping for one second")
            self._clear_request_bucket()
            time.sleep(1)

        self._request_bucket.append(datetime.now())

        full_url = "/".join((self.BASE_URL, url.lstrip("/")))
        response = super().request(method, full_url, *args, **kwargs)
        try:
            response.raise_for_status()
        except HTTPError as e:
            if e.response.status_code == 429 and retry_on_rate_limit:
                logger.warning("We hit the rate limit.")
                try:
                    retry_after: int = int(e.response.headers.get("Retry-After", 5))
                except ValueError:
                    retry_after: int = 10
                logger.warning(f"Waiting {retry_after} seconds to try again...")
                time.sleep(retry_after)
                return self.request(method, url, retry_on_rate_limit=False, *args, **kwargs)
            else:
                raise e
        return response

    def get_orders(self, **params) -> List[Order]:
        response = self.request("GET", "order", params=params)
        response.raise_for_status()
        return [Order(**order_data) for order_data in response.json()]

    def get_order_shipments(self, order: Order, **params) -> List[Shipment]:
        response = self.request("GET", f"order/{order.id}/shipment", params=params)
        response.raise_for_status()
        return [Shipment(**shipment_data) for shipment_data in response.json()]

    def get_shipment_events(self, shipment: Shipment, **params) -> List[ShipmentEvent]:
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

    def get_inventory_items(self, **params) -> List[InventoryItem]:
        response = self.request("GET", "inventory", params=params)
        response.raise_for_status()
        return [InventoryItem(**item_data) for item_data in response.json()]

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

    def iterate_inventory_items(self, **params) -> Iterator[InventoryItem]:
        params.pop("page", None)
        params.pop("limit", None)

        page = 1
        while inventory_items := self.get_inventory_items(
            page=page, limit=self.MAX_PAGE_SIZE, **params
        ):
            logger.debug(f"Getting page {page} of inventory_items")
            for inventory_item in inventory_items:
                yield inventory_item
            page += 1
