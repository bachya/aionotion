"""Define endpoints for interacting with users."""

from __future__ import annotations

from typing import TYPE_CHECKING

from aionotion.user.models import User as UserModel
from aionotion.user.models import (
    UserInformationResponse,
    UserPreferences,
    UserPreferencesResponse,
)

if TYPE_CHECKING:
    from aionotion.client import Client


class User:  # pylint: disable=too-few-public-methods
    """Define an object to interact with user endpoints."""

    def __init__(self, client: Client) -> None:
        """Initialize.

        Args:
            client: The aionotion client
        """
        self._client = client

    async def async_info(self) -> UserModel:
        """Get the user's information.

        Returns:
            A validated API response payload.
        """
        response: UserInformationResponse = (
            await self._client.async_request_and_validate(
                "get",
                f"/users/{self._client.user_uuid}",
                UserInformationResponse,
            )
        )
        return response.users

    async def async_preferences(self) -> UserPreferences:
        """Get user preferences.

        Returns:
            A validated API response payload.
        """
        response: UserPreferencesResponse = (
            await self._client.async_request_and_validate(
                "get",
                f"/users/{self._client.user_uuid}/user_preferences",
                UserPreferencesResponse,
            )
        )
        return response.user_preferences
