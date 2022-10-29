"""Define endpoints for interacting with devices (phones, etc. with Notion)."""
from __future__ import annotations

from collections.abc import Awaitable, Callable
from typing import Any, cast


class Device:
    """Define an object to interact with all endpoints."""

    def __init__(self, request: Callable[..., Awaitable[dict[str, Any]]]) -> None:
        """Initialize.

        Args:
            request: The request method from the Client object.
        """
        self._request = request

    async def async_all(self) -> list[dict[str, Any]]:
        """Get all devices.

        Returns:
            An API response payload.
        """
        resp = await self._request("get", "devices")
        return cast(list[dict[str, Any]], resp["devices"])

    async def async_create(self, attributes: dict[str, Any]) -> dict[str, Any]:
        """Create a device with a specific attribute payload.

        Args:
            attributes: The attributes to assign to the new device.

        Returns:
            An API response payload.
        """
        resp = await self._request("post", "devices", json={"devices": attributes})
        return cast(dict[str, Any], resp["devices"])

    async def async_delete(self, device_id: int) -> None:
        """Delete a device by ID.

        Args:
            device_id: The ID of the device to delete.
        """
        await self._request("delete", f"devices/{device_id}")

    async def async_get(self, device_id: int) -> dict[str, Any]:
        """Get a device by ID.

        Args:
            device_id: The ID of the device to get.

        Returns:
            An API response payload.
        """
        resp = await self._request("get", f"devices/{device_id}")
        return cast(dict[str, Any], resp["devices"])
