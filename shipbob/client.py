import os
from typing import List

from requests import Session

from .models import Order


class ShipBob(Session):
    BASE_URL = "https://api.shipbob.com/1.0"

    ACCESS_TOKEN = os.getenv("SHIPBOB_ACCESS_TOKEN")

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
