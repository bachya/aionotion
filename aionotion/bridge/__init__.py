"""Define endpoints for interacting with bridges."""

from __future__ import annotations

from typing import TYPE_CHECKING

from aionotion.bridge.models import Bridge as BridgeModel
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

    async def async_all(self) -> list[BridgeModel]:
        """Get all bridges.

        Returns:
            A validated API response payload.
        """
        response: BridgeAllResponse = await self._client.async_request_and_validate(
            "get", "/base_stations", BridgeAllResponse
        )
        return response.base_stations

    async def async_get(self, bridge_id: int) -> BridgeModel:
        """Get a bridge by ID.

        Args:
            bridge_id: The ID of the bridge to get.

        Returns:
            A validated API response payload.
        """
        response: BridgeGetResponse = await self._client.async_request_and_validate(
            "get", f"/base_stations/{bridge_id}", BridgeGetResponse
        )
        return response.base_stations
