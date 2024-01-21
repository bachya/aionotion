"""Define endpoints for interacting with systems (accounts)."""
from __future__ import annotations

from typing import TYPE_CHECKING

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
            "get", "/systems", SystemAllResponse
        )

    async def async_get(self, system_id: int) -> SystemGetResponse:
        """Get a system by ID.

        Args:
            system_id: The ID of the system to get.

        Returns:
            An API response payload.
        """
        return await self._client.async_request_and_validate(
            "get", f"/systems/{system_id}", SystemGetResponse
        )
