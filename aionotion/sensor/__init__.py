"""Define endpoints for interacting with sensors."""
from __future__ import annotations

from collections.abc import Awaitable, Callable
from typing import Any, cast

from aionotion.helpers.typing import BaseModelT
from aionotion.sensor.models import Listener, ListenerAllResponse
from aionotion.sensor.models import Sensor as SensorModel
from aionotion.sensor.models import SensorAllResponse, SensorGetResponse


class Sensor:
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

    async def async_all(self) -> list[SensorModel]:
        """Get all sensors.

        Returns:
            A validated API response payload.
        """
        resp = cast(
            SensorAllResponse,
            await self._request_and_validate("get", "sensors", SensorAllResponse),
        )
        return resp.sensors

    async def async_create(self, attributes: dict[str, Any]) -> SensorModel:
        """Create a sensor with a specific attribute payload.

        Args:
            attributes: The attributes to assign to the new sensor.

        Returns:
            A validated API response payload.
        """
        resp = cast(
            SensorGetResponse,
            await self._request_and_validate(
                "post", "sensors", SensorGetResponse, json={"sensors": attributes}
            ),
        )
        return resp.sensor

    async def async_delete(self, sensor_id: int) -> None:
        """Delete a sensor by ID.

        Args:
            sensor_id: The ID of the sensor to delete.
        """
        await self._request("delete", f"sensors/{sensor_id}")

    async def async_get(self, sensor_id: int) -> SensorModel:
        """Get a sensor by ID.

        Args:
            sensor_id: The ID of the sensor to get.

        Returns:
            A validated API response payload.
        """
        resp = cast(
            SensorGetResponse,
            await self._request_and_validate(
                "get", f"sensors/{sensor_id}", SensorGetResponse
            ),
        )
        return resp.sensor

    async def async_listeners(self) -> list[Listener]:
        """Get all listeners for all sensors.

        Returns:
            A validated API response payload.
        """
        resp = cast(
            ListenerAllResponse,
            await self._request_and_validate(
                "get", "sensor/listeners", ListenerAllResponse
            ),
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
        resp = cast(
            ListenerAllResponse,
            await self._request_and_validate(
                "get", f"sensors/{sensor_uuid}/listeners", ListenerAllResponse
            ),
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
        resp = cast(
            SensorGetResponse,
            await self._request_and_validate(
                "put",
                f"sensors/{sensor_id}",
                SensorGetResponse,
                json={"sensors": new_attributes},
            ),
        )
        return resp.sensor
