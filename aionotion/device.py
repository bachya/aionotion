"""Define endpoints for interacting with devices (phones, etc. with Notion)."""
from typing import Callable


class Device:
    """Define an object to interact with all endpoints."""

    def __init__(self, request: Callable) -> None:
        """Initialize."""
        self._request: Callable = request

    async def async_all(self) -> list:
        """Get all devices."""
        resp: dict = await self._request("get", "devices")
        return resp["devices"]

    async def async_create(self, attributes: dict) -> dict:
        """Create a device with a specific attribute payload."""
        resp: dict = await self._request(
            "post", "devices", json={"devices": attributes}
        )
        return resp["devices"]

    async def async_delete(self, device_id: int) -> None:
        """Delete a device by ID."""
        await self._request("delete", f"devices/{device_id}")

    async def async_get(self, device_id: int) -> dict:
        """Get a device by ID."""
        resp: dict = await self._request("get", f"devices/{device_id}")
        return resp["devices"]
