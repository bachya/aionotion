"""Define endpoints for interacting with devices (phones, etc. with Notion)."""
from __future__ import annotations

from collections.abc import Awaitable, Callable
from typing import Any, cast

from aionotion.device.models import Device as DeviceModel
from aionotion.device.models import DeviceAllResponse, DeviceGetResponse
from aionotion.helpers.typing import BaseModelT


class Device:
    """Define an object to interact with all endpoints."""

    def __init__(
        self,
        request: Callable[..., Awaitable[dict[str, Any]]],
        request_and_validate: Callable[..., Awaitable[BaseModelT]],
    ) -> None:
        """Initialize.

        Args:
            request: The _request method from the Client.
            request_and_validated: The _request_and_validate method from the Client.
        """
        self._request = request
        self._request_and_validate = request_and_validate

    async def async_all(self) -> list[DeviceModel]:
        """Get all devices.

        Returns:
            A validated API response payload.
        """
        resp = cast(
            DeviceAllResponse,
            await self._request_and_validate("get", "devices", DeviceAllResponse),
        )
        return resp.devices

    async def async_create(self, attributes: dict[str, Any]) -> DeviceModel:
        """Create a device with a specific attribute payload.

        Args:
            attributes: The attributes to assign to the new device.

        Returns:
            A validated API response payload.
        """
        resp = cast(
            DeviceGetResponse,
            await self._request_and_validate(
                "post", "devices", DeviceGetResponse, json={"devices": attributes}
            ),
        )
        return resp.device

    async def async_delete(self, device_id: int) -> None:
        """Delete a device by ID.

        Args:
            device_id: The ID of the device to delete.
        """
        await self._request("delete", f"devices/{device_id}")

    async def async_get(self, device_id: int) -> DeviceModel:
        """Get a device by ID.

        Args:
            device_id: The ID of the device to get.

        Returns:
            A validated API response payload.
        """
        resp = cast(
            DeviceGetResponse,
            await self._request_and_validate(
                "get", f"devices/{device_id}", DeviceGetResponse
            ),
        )
        return resp.device
