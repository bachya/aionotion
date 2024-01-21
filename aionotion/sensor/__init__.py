"""Define endpoints for interacting with sensors."""
from __future__ import annotations

from typing import TYPE_CHECKING

from aionotion.sensor.models import (
    ListenerAllResponse,
    SensorAllResponse,
    SensorGetResponse,
)

if TYPE_CHECKING:
    from aionotion.client import Client


class Sensor:
    """Define an object to interact with sensor endpoints."""

    def __init__(self, client: Client) -> None:
        """Initialize.

        Args:
            client: The aionotion client
        """
        self._client = client

    async def async_all(self) -> SensorAllResponse:
        """Get all sensors.

        Returns:
            A validated API response payload.
        """
        return await self._client.async_request_and_validate(
            "get", "/sensors", SensorAllResponse
        )

    async def async_get(self, sensor_id: int) -> SensorGetResponse:
        """Get a sensor by ID.

        Args:
            sensor_id: The ID of the sensor to get.

        Returns:
            A validated API response payload.
        """
        return await self._client.async_request_and_validate(
            "get", f"/sensors/{sensor_id}", SensorGetResponse
        )

    async def async_listeners(self) -> ListenerAllResponse:
        """Get all listeners for all sensors.

        Returns:
            A validated API response payload.
        """
        return await self._client.async_request_and_validate(
            "get", "/sensor/listeners", ListenerAllResponse
        )
