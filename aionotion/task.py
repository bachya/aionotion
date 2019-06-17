"""Define endpoints for interacting with tasks (monitored conditions)."""
from typing import Callable


class Task:  # pylint: disable=too-few-public-methods
    """Define an object to interact with all endpoints."""

    def __init__(self, request: Callable) -> None:
        """Initialize."""
        self._request = request

    async def async_all(self) -> list:
        """Get all tasks."""
        resp = await self._request("get", "tasks")
        return resp["tasks"]
