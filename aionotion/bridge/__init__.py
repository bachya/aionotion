"""Define endpoints for interacting with bridges."""
from __future__ import annotations

from collections.abc import Awaitable, Callable
from typing import Any, cast

from aionotion.bridge.models import Bridge as BridgeModel
from aionotion.bridge.models import BridgeAllResponse, BridgeGetResponse
from aionotion.helpers.typing import BaseModelT


class Bridge:
    """Define an object to interact with all endpoints."""

    def __init__(
        self,
        request: Callable[..., Awaitable[dict[str, Any]]],
        request_and_validate: Callable[..., Awaitable[BaseModelT]],
    ) -> None:
        """Initialize.

        Args:
            request: The _request method from the Client.
            request_and_validated: The _request_and_validate method from the Client.
        """
        self._request = request
        self._request_and_validate = request_and_validate

    async def async_all(self) -> list[BridgeModel]:
        """Get all bridges.

        Returns:
            A validated API response payload.
        """
        resp = cast(
            BridgeAllResponse,
            await self._request_and_validate("get", "base_stations", BridgeAllResponse),
        )
        return resp.bridges

    async def async_create(self, attributes: dict[str, Any]) -> BridgeModel:
        """Create a bridge with a specific attribute payload.

        Args:
            attributes: The attributes to assign to the new bridge.

        Returns:
            A validated API response payload.
        """
        resp = cast(
            BridgeGetResponse,
            await self._request_and_validate(
                "post",
                "base_stations",
                BridgeGetResponse,
                json={"base_stations": attributes},
            ),
        )
        return resp.bridge

    async def async_delete(self, bridge_id: int) -> None:
        """Delete a bridge by ID.

        Args:
            bridge_id: The ID of the bridge to delete.
        """
        await self._request("delete", f"base_stations/{bridge_id}")

    async def async_get(self, bridge_id: int) -> BridgeModel:
        """Get a bridge by ID.

        Args:
            bridge_id: The ID of the bridge to get.

        Returns:
            A validated API response payload.
        """
        resp = cast(
            BridgeGetResponse,
            await self._request_and_validate(
                "get", f"base_stations/{bridge_id}", BridgeGetResponse
            ),
        )
        return resp.bridge

    async def async_reset(self, bridge_id: int) -> BridgeModel:
        """Reset a bridge (clear its wifi credentials) by ID.

        Args:
            bridge_id: The ID of the bridge to reset.

        Returns:
            A validated API response payload.
        """
        resp = cast(
            BridgeGetResponse,
            await self._request_and_validate(
                "put", f"base_stations/{bridge_id}/reset", BridgeGetResponse
            ),
        )
        return resp.bridge

    async def async_update(
        self, bridge_id: int, new_attributes: dict[str, Any]
    ) -> BridgeModel:
        """Update a bridge with a specific attribute payload.

        Args:
            bridge_id: The ID of the bridge to update.
            new_attributes: The new attributes to give the bridge.

        Returns:
            A validated API response payload.
        """
        resp = cast(
            BridgeGetResponse,
            await self._request_and_validate(
                "put",
                f"base_stations/{bridge_id}",
                BridgeGetResponse,
                json={"base_stations": new_attributes},
            ),
        )
        return resp.bridge
