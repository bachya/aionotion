"""Define endpoints for interacting with bridges."""
from typing import Any, Callable, Dict, List


class Bridge:  # pylint: disable=too-few-public-methods
    """Define an object to interact with all endpoints."""

    def __init__(self, request: Callable) -> None:
        """Initialize."""
        self._request = request

    async def async_all(self) -> List[Dict[str, Any]]:
        """Get all bridges."""
        resp: dict = await self._request("get", "base_stations")
        return resp["base_stations"]

    async def async_create(self, attributes: Dict[str, Any]) -> Dict[str, Any]:
        """Create a bridge with a specific attribute payload."""
        resp: dict = await self._request(
            "post", "base_stations", json={"base_stations": attributes}
        )
        return resp["base_stations"]

    async def async_delete(self, bridge_id: int) -> None:
        """Delete a bridge by ID."""
        await self._request("delete", f"base_stations/{bridge_id}")

    async def async_get(self, bridge_id: int) -> Dict[str, Any]:
        """Get a bridge by ID."""
        resp: dict = await self._request("get", f"base_stations/{bridge_id}")
        return resp["base_stations"]

    async def async_reset(self, bridge_id: int) -> Dict[str, Any]:
        """Reset a bridge (clear its wifi credentials) by ID."""
        resp: dict = await self._request("put", f"base_stations/{bridge_id}/reset")
        return resp["base_stations"]

    async def async_update(
        self, bridge_id: int, new_attributes: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update a bridge with a specific attribute payload."""
        resp: dict = await self._request(
            "put", f"base_stations/{bridge_id}", json={"base_stations": new_attributes}
        )
        return resp["base_stations"]
