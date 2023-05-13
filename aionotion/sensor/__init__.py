"""Define endpoints for interacting with sensors."""
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from aionotion.sensor.models import Listener, ListenerAllResponse
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
        resp: SensorAllResponse = await self._client.async_request_and_validate(
            "get", "sensors", SensorAllResponse
        )
        return resp.sensors

    async def async_create(self, attributes: dict[str, Any]) -> SensorModel:
        """Create a sensor with a specific attribute payload.

        Args:
            attributes: The attributes to assign to the new sensor.

        Returns:
            A validated API response payload.
        """
        resp: SensorGetResponse = await self._client.async_request_and_validate(
            "post", "sensors", SensorGetResponse, json={"sensors": attributes}
        )
        return resp.sensor

    async def async_delete(self, sensor_id: int) -> None:
        """Delete a sensor by ID.

        Args:
            sensor_id: The ID of the sensor to delete.
        """
        await self._client.async_request("delete", f"sensors/{sensor_id}")

    async def async_get(self, sensor_id: int) -> SensorModel:
        """Get a sensor by ID.

        Args:
            sensor_id: The ID of the sensor to get.

        Returns:
            A validated API response payload.
        """
        resp: SensorGetResponse = await self._client.async_request_and_validate(
            "get", f"sensors/{sensor_id}", SensorGetResponse
        )
        return resp.sensor

    async def async_listeners(self) -> list[Listener]:
        """Get all listeners for all sensors.

        Returns:
            A validated API response payload.
        """
        resp: ListenerAllResponse = await self._client.async_request_and_validate(
            "get", "sensor/listeners", ListenerAllResponse
        )
        return resp.listeners

    async def async_listeners_for_sensor(self, sensor_uuid: str) -> list[Listener]:
        """Get all listeners for a sensor by UUID.

        Note that unlike other sensor endpoints, the sensor ID won't work here; the
        sensor UUID is required.

        Args:
            sensor_uuid: The UUID of the sensor to get.

        Returns:
            A validated API response payload.
        """
        resp: ListenerAllResponse = await self._client.async_request_and_validate(
            "get", f"sensors/{sensor_uuid}/listeners", ListenerAllResponse
        )
        return resp.listeners

    async def async_update(
        self, sensor_id: int, new_attributes: dict[str, Any]
    ) -> SensorModel:
        """Update a sensor with a specific attribute payload.

        Args:
            sensor_id: The ID of the sensor to update.
            new_attributes: The new attributes to give the sensor.

        Returns:
            A validated API response payload.
        """
        resp: SensorGetResponse = await self._client.async_request_and_validate(
            "put",
            f"sensors/{sensor_id}",
            SensorGetResponse,
            json={"sensors": new_attributes},
        )
        return resp.sensor
