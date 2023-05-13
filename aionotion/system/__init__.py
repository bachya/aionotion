"""Define endpoints for interacting with systems (accounts)."""
from __future__ import annotations

from typing import TYPE_CHECKING, Any

from aionotion.system.models import SystemAllResponse, SystemGetResponse

if TYPE_CHECKING:
    from aionotion.client import Client


class System:
    """Define an object to interact with system endpoints."""

    def __init__(self, client: Client) -> None:
        """Initialize.

        Args:
            client: The aionotion client
        """
        self._client = client

    async def async_all(self) -> SystemAllResponse:
        """Get all systems.

        Returns:
            An API response payload.
        """
        return await self._client.async_request_and_validate(
            "get", "systems", SystemAllResponse
        )

    async def async_create(self, attributes: dict[str, Any]) -> SystemGetResponse:
        """Create a system with a specific attribute payload.

        Args:
            attributes: The attributes to assign to the new system.

        Returns:
            An API response payload.
        """
        return await self._client.async_request_and_validate(
            "post", "systems", SystemGetResponse, json={"systems": attributes}
        )

    async def async_delete(self, system_id: int) -> None:
        """Delete a system by ID.

        Args:
            system_id: The ID of the system to delete.
        """
        await self._client.async_request("delete", f"systems/{system_id}")

    async def async_get(self, system_id: int) -> SystemGetResponse:
        """Get a system by ID.

        Args:
            system_id: The ID of the system to get.

        Returns:
            An API response payload.
        """
        return await self._client.async_request_and_validate(
            "get", f"systems/{system_id}", SystemGetResponse
        )

    async def async_update(
        self, system_id: int, new_attributes: dict[str, Any]
    ) -> SystemGetResponse:
        """Update a system with a specific attribute payload.

        Args:
            system_id: The ID of the system to update.
            new_attributes: The new attributes to give the system.

        Returns:
            An API response payload.
        """
        return await self._client.async_request_and_validate(
            "put",
            f"systems/{system_id}",
            SystemGetResponse,
            json={"systems": new_attributes},
        )
