"""Define endpoints for interacting with sensors."""
from typing import Callable


class Sensor:  # pylint: disable=too-few-public-methods
    """Define an object to interact with all endpoints."""

    def __init__(self, request: Callable) -> None:
        """Initialize."""
        self._request = request

    async def async_all(self) -> list:
        """Get all sensors."""
        resp = await self._request("get", "sensors")
        return resp["sensors"]

    async def async_create(self, attributes: dict) -> dict:
        """Create a sensor with a specific attribute payload."""
        resp = await self._request("post", "sensors", json={"sensors": attributes})
        return resp["sensors"]

    async def async_delete(self, sensor_id: int) -> None:
        """Delete a sensor by ID."""
        await self._request("delete", "sensors/{0}".format(sensor_id))

    async def async_get(self, sensor_id: int) -> dict:
        """Get a sensor by ID."""
        resp = await self._request("get", "sensors/{0}".format(sensor_id))
        return resp["sensors"]

    async def async_update(self, sensor_id: int, new_attributes: dict) -> dict:
        """Update a sensor with a specific attribute payload."""
        resp = await self._request(
            "put", "sensors/{0}".format(sensor_id), json={"sensors": new_attributes}
        )
        return resp["sensors"]
