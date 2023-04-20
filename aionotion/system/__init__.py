"""Define endpoints for interacting with systems (accounts)."""
from collections.abc import Awaitable, Callable
from typing import Any, cast

from aionotion.helpers.typing import BaseModelT
from aionotion.system.models import System as SystemModel
from aionotion.system.models import SystemAllResponse, SystemGetResponse


class System:
    """Define an object to interact with all endpoints."""

    def __init__(
        self,
        request: Callable[..., Awaitable[dict[str, Any]]],
        request_and_validate: Callable[..., Awaitable[BaseModelT]],
    ) -> None:
        """Initialize.

        Args:
            request: The request method from the Client object.
        """
        self._request = request
        self._request_and_validate = request_and_validate

    async def async_all(self) -> list[SystemModel]:
        """Get all systems.

        Returns:
            An API response payload.
        """
        resp = cast(
            SystemAllResponse,
            await self._request_and_validate("get", "systems", SystemAllResponse),
        )
        return resp.systems

    async def async_create(self, attributes: dict[str, Any]) -> SystemModel:
        """Create a system with a specific attribute payload.

        Args:
            attributes: The attributes to assign to the new system.

        Returns:
            An API response payload.
        """
        resp = cast(
            SystemGetResponse,
            await self._request_and_validate(
                "post", "systems", SystemGetResponse, json={"systems": attributes}
            ),
        )
        return resp.system

    async def async_delete(self, system_id: int) -> None:
        """Delete a system by ID.

        Args:
            system_id: The ID of the system to delete.
        """
        await self._request("delete", f"systems/{system_id}")

    async def async_get(self, system_id: int) -> SystemModel:
        """Get a system by ID.

        Args:
            system_id: The ID of the system to get.

        Returns:
            An API response payload.
        """
        resp = cast(
            SystemGetResponse,
            await self._request_and_validate(
                "get", f"systems/{system_id}", SystemGetResponse
            ),
        )
        return resp.system

    async def async_update(
        self, system_id: int, new_attributes: dict[str, Any]
    ) -> SystemModel:
        """Update a system with a specific attribute payload.

        Args:
            system_id: The ID of the system to update.
            new_attributes: The new attributes to give the system.

        Returns:
            An API response payload.
        """
        resp = cast(
            SystemGetResponse,
            await self._request_and_validate(
                "put",
                f"systems/{system_id}",
                SystemGetResponse,
                json={"systems": new_attributes},
            ),
        )
        return resp.system
