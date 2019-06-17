"""Define endpoints for interacting with bridges."""
from typing import Callable


class Bridge:  # pylint: disable=too-few-public-methods
    """Define an object to interact with all endpoints."""

    def __init__(self, request: Callable) -> None:
        """Initialize."""
        self._request = request

    async def async_all(self) -> list:
        """Get all bridges."""
        resp = await self._request("get", "base_stations")
        return resp["base_stations"]
