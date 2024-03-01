"""Define endpoints for interacting with sensors."""

from __future__ import annotations

from typing import TYPE_CHECKING

from aionotion.sensor.models import Sensor as SensorModel
from aionotion.sensor.models import SensorAllResponse, SensorGetResponse

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

    async def async_all(self) -> list[SensorModel]:
        """Get all sensors.

        Returns:
            A validated API response payload.
        """
        response: SensorAllResponse = await self._client.async_request_and_validate(
            "get", "/sensors", SensorAllResponse
        )
        return response.sensors

    async def async_get(self, sensor_id: int) -> SensorModel:
        """Get a sensor by ID.

        Args:
            sensor_id: The ID of the sensor to get.

        Returns:
            A validated API response payload.
        """
        response: SensorGetResponse = await self._client.async_request_and_validate(
            "get", f"/sensors/{sensor_id}", SensorGetResponse
        )
        return response.sensors
