"""Define endpoints for interacting with bridges."""
from __future__ import annotations

from typing import TYPE_CHECKING

from aionotion.bridge.models import BridgeAllResponse, BridgeGetResponse

if TYPE_CHECKING:
    from aionotion.client import Client


class Bridge:
    """Define an object to interact with bridge endpoints."""

    def __init__(self, client: Client) -> None:
        """Initialize.

        Args:
            client: The aionotion client
        """
        self._client = client

    async def async_all(self) -> BridgeAllResponse:
        """Get all bridges.

        Returns:
            A validated API response payload.
        """
        return await self._client.async_request_and_validate(
            "get", "/base_stations", BridgeAllResponse
        )

    async def async_get(self, bridge_id: int) -> BridgeGetResponse:
        """Get a bridge by ID.

        Args:
            bridge_id: The ID of the bridge to get.

        Returns:
            A validated API response payload.
        """
        return await self._client.async_request_and_validate(
            "get", f"/base_stations/{bridge_id}", BridgeGetResponse
        )
