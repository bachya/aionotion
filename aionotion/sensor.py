"""Define endpoints for interacting with sensors."""
from __future__ import annotations

from collections.abc import Awaitable, Callable
from typing import Any, cast


class Sensor:
    """Define an object to interact with all endpoints."""

    def __init__(self, request: Callable[..., Awaitable[dict[str, Any]]]) -> None:
        """Initialize.

        Args:
            request: The request method from the Client object.
        """
        self._request = request

    async def async_all(self) -> list[dict[str, Any]]:
        """Get all sensors.

        Returns:
            An API response payload.
        """
        resp = await self._request("get", "sensors")
        return cast(list[dict[str, Any]], resp["sensors"])

    async def async_create(self, attributes: dict[str, Any]) -> dict[str, Any]:
        """Create a sensor with a specific attribute payload.

        Args:
            attributes: The attributes to assign to the new sensor.

        Returns:
            An API response payload.
        """
        resp = await self._request("post", "sensors", json={"sensors": attributes})
        return cast(dict[str, Any], resp["sensors"])

    async def async_delete(self, sensor_id: int) -> None:
        """Delete a sensor by ID.

        Args:
            sensor_id: The ID of the sensor to delete.
        """
        await self._request("delete", f"sensors/{sensor_id}")

    async def async_get(self, sensor_id: int) -> dict[str, Any]:
        """Get a sensor by ID.

        Args:
            sensor_id: The ID of the sensor to get.

        Returns:
            An API response payload.
        """
        resp = await self._request("get", f"sensors/{sensor_id}")
        return cast(dict[str, Any], resp["sensors"])

    async def async_update(
        self, sensor_id: int, new_attributes: dict[str, Any]
    ) -> dict[str, Any]:
        """Update a sensor with a specific attribute payload.

        Args:
            sensor_id: The ID of the sensor to update.
            new_attributes: The new attributes to give the sensor.

        Returns:
            An API response payload.
        """
        resp = await self._request(
            "put", f"sensors/{sensor_id}", json={"sensors": new_attributes}
        )
        return cast(dict[str, Any], resp["sensors"])
