"""Define endpoints for interacting with systems (accounts)."""
from collections.abc import Awaitable, Callable
from typing import Any, cast


class System:
    """Define an object to interact with all endpoints."""

    def __init__(self, request: Callable[..., Awaitable[dict[str, Any]]]) -> None:
        """Initialize.

        Args:
            request: The request method from the Client object.
        """
        self._request = request

    async def async_all(self) -> list[dict[str, Any]]:
        """Get all systems.

        Returns:
            An API response payload.
        """
        resp = await self._request("get", "systems")
        return cast(list[dict[str, Any]], resp["systems"])

    async def async_create(self, attributes: dict[str, Any]) -> dict[str, Any]:
        """Create a system with a specific attribute payload.

        Args:
            attributes: The attributes to assign to the new system.

        Returns:
            An API response payload.
        """
        resp = await self._request("post", "systems", json={"systems": attributes})
        return cast(dict[str, Any], resp["systems"])

    async def async_delete(self, system_id: int) -> None:
        """Delete a system by ID.

        Args:
            system_id: The ID of the system to delete.
        """
        await self._request("delete", f"systems/{system_id}")

    async def async_get(self, system_id: int) -> dict[str, Any]:
        """Get a system by ID.

        Args:
            system_id: The ID of the system to get.

        Returns:
            An API response payload.
        """
        resp = await self._request("get", f"systems/{system_id}")
        return cast(dict[str, Any], resp["systems"])

    async def async_update(
        self, system_id: int, new_attributes: dict[str, Any]
    ) -> dict[str, Any]:
        """Update a system with a specific attribute payload.

        Args:
            system_id: The ID of the system to update.
            new_attributes: The new attributes to give the system.

        Returns:
            An API response payload.
        """
        resp = await self._request(
            "put", f"systems/{system_id}", json={"systems": new_attributes}
        )
        return cast(dict[str, Any], resp["systems"])
