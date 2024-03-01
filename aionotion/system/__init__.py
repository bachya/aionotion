"""Define endpoints for interacting with systems (accounts)."""

from __future__ import annotations

from typing import TYPE_CHECKING

from aionotion.system.models import System as SystemModel
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

    async def async_all(self) -> list[SystemModel]:
        """Get all systems.

        Returns:
            An API response payload.
        """
        response: SystemAllResponse = await self._client.async_request_and_validate(
            "get", "/systems", SystemAllResponse
        )
        return response.systems

    async def async_get(self, system_id: int) -> SystemModel:
        """Get a system by ID.

        Args:
            system_id: The ID of the system to get.

        Returns:
            An API response payload.
        """
        response: SystemGetResponse = await self._client.async_request_and_validate(
            "get", f"/systems/{system_id}", SystemGetResponse
        )
        return response.systems
