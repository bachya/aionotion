"""Define endpoints for interacting with bridges."""
from typing import Callable


class Bridge:  # pylint: disable=too-few-public-methods
    """Define an object to interact with all endpoints."""

    def __init__(self, request: Callable) -> None:
        """Initialize."""
        self._request: Callable = request

    async def async_all(self) -> list:
        """Get all bridges."""
        resp: dict = await self._request("get", "base_stations")
        return resp["base_stations"]

    async def async_create(self, attributes: dict) -> dict:
        """Create a bridge with a specific attribute payload."""
        resp: dict = await self._request(
            "post", "base_stations", json={"base_stations": attributes}
        )
        return resp["base_stations"]

    async def async_delete(self, bridge_id: int) -> None:
        """Delete a bridge by ID."""
        await self._request("delete", f"base_stations/{bridge_id}")

    async def async_get(self, bridge_id: int) -> dict:
        """Get a bridge by ID."""
        resp: dict = await self._request("get", f"base_stations/{bridge_id}")
        return resp["base_stations"]

    async def async_reset(self, bridge_id: int) -> dict:
        """Reset a bridge (clear its wifi credentials) by ID."""
        resp: dict = await self._request("put", f"base_stations/{bridge_id}/reset")
        return resp["base_stations"]

    async def async_update(self, bridge_id: int, new_attributes: dict) -> dict:
        """Update a bridge with a specific attribute payload."""
        resp: dict = await self._request(
            "put", f"base_stations/{bridge_id}", json={"base_stations": new_attributes}
        )
        return resp["base_stations"]
