"""Define endpoints for interacting with bridges."""
from __future__ import annotations

from collections.abc import Awaitable, Callable
from typing import Any, cast


class Bridge:
    """Define an object to interact with all endpoints."""

    def __init__(self, request: Callable[..., Awaitable[dict[str, Any]]]) -> None:
        """Initialize.

        Args:
            request: The request method from the Client object.
        """
        self._request = request

    async def async_all(self) -> list[dict[str, Any]]:
        """Get all bridges.

        Returns:
            An API response payload.
        """
        resp = await self._request("get", "base_stations")
        return cast(list[dict[str, Any]], resp["base_stations"])

    async def async_create(self, attributes: dict[str, Any]) -> dict[str, Any]:
        """Create a bridge with a specific attribute payload.

        Args:
            attributes: The attributes to assign to the new bridge.

        Returns:
            An API response payload.
        """
        resp = await self._request(
            "post", "base_stations", json={"base_stations": attributes}
        )
        return cast(dict[str, Any], resp["base_stations"])

    async def async_delete(self, bridge_id: int) -> None:
        """Delete a bridge by ID.

        Args:
            bridge_id: The ID of the bridge to delete.
        """
        await self._request("delete", f"base_stations/{bridge_id}")

    async def async_get(self, bridge_id: int) -> dict[str, Any]:
        """Get a bridge by ID.

        Args:
            bridge_id: The ID of the bridge to get.

        Returns:
            An API response payload.
        """
        resp = await self._request("get", f"base_stations/{bridge_id}")
        return cast(dict[str, Any], resp["base_stations"])

    async def async_reset(self, bridge_id: int) -> dict[str, Any]:
        """Reset a bridge (clear its wifi credentials) by ID.

        Args:
            bridge_id: The ID of the bridge to reset.

        Returns:
            An API response payload.
        """
        resp = await self._request("put", f"base_stations/{bridge_id}/reset")
        return cast(dict[str, Any], resp["base_stations"])

    async def async_update(
        self, bridge_id: int, new_attributes: dict[str, Any]
    ) -> dict[str, Any]:
        """Update a bridge with a specific attribute payload.

        Args:
            bridge_id: The ID of the bridge to update.
            new_attributes: The new attributes to give the bridge.

        Returns:
            An API response payload.
        """
        resp = await self._request(
            "put", f"base_stations/{bridge_id}", json={"base_stations": new_attributes}
        )
        return cast(dict[str, Any], resp["base_stations"])
