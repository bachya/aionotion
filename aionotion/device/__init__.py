"""Define endpoints for interacting with devices (phones, etc. with Notion)."""
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from aionotion.device.models import DeviceAllResponse, DeviceGetResponse

if TYPE_CHECKING:
    from aionotion.client import Client


class Device:
    """Define an object to interact with device endpoints."""

    def __init__(self, client: Client) -> None:
        """Initialize.

        Args:
            client: The aionotion client
        """
        self._client = client

    async def async_all(self) -> DeviceAllResponse:
        """Get all devices.

        Returns:
            A validated API response payload.
        """
        return await self._client.async_request_and_validate(
            "get", "devices", DeviceAllResponse
        )

    async def async_create(self, attributes: dict[str, Any]) -> DeviceGetResponse:
        """Create a device with a specific attribute payload.

        Args:
            attributes: The attributes to assign to the new device.

        Returns:
            A validated API response payload.
        """
        return await self._client.async_request_and_validate(
            "post", "devices", DeviceGetResponse, json={"devices": attributes}
        )

    async def async_delete(self, device_id: int) -> None:
        """Delete a device by ID.

        Args:
            device_id: The ID of the device to delete.
        """
        await self._client.async_request("delete", f"devices/{device_id}")

    async def async_get(self, device_id: int) -> DeviceGetResponse:
        """Get a device by ID.

        Args:
            device_id: The ID of the device to get.

        Returns:
            A validated API response payload.
        """
        return await self._client.async_request_and_validate(
            "get", f"devices/{device_id}", DeviceGetResponse
        )
