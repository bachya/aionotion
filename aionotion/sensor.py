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
