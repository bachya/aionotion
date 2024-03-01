"""Define endpoints for interacting with listeners."""

from __future__ import annotations

from typing import TYPE_CHECKING

from aionotion.listener.models import Listener as ListenerModel
from aionotion.listener.models import (
    ListenerAllResponse,
    ListenerDefinition,
    ListenerDefinitionResponse,
)

if TYPE_CHECKING:
    from aionotion.client import Client


class Listener:
    """Define an object to interact with sensor endpoints."""

    def __init__(self, client: Client) -> None:
        """Initialize.

        Args:
            client: The aionotion client
        """
        self._client = client

    async def async_all(self) -> list[ListenerModel]:
        """Get all listeners.

        Returns:
            A validated API response payload.
        """
        response: ListenerAllResponse = await self._client.async_request_and_validate(
            "get", "/sensor/listeners", ListenerAllResponse
        )
        return response.listeners

    async def async_definitions(self) -> list[ListenerDefinition]:
        """Get all listener definitions.

        Returns:
            A validated API response payload.
        """
        response: ListenerDefinitionResponse = (
            await self._client.async_request_and_validate(
                "get", "/listener_definitions", ListenerDefinitionResponse
            )
        )
        return response.listener_definitions
