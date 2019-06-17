"""Define endpoints for interacting with systems (accounts)."""
from typing import Callable


class System:  # pylint: disable=too-few-public-methods
    """Define an object to interact with all endpoints."""

    def __init__(self, request: Callable) -> None:
        """Initialize."""
        self._request = request

    async def async_all(self) -> list:
        """Get all systems."""
        resp = await self._request("get", "systems")
        return resp["systems"]
