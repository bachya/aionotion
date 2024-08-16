"""Define tests for users."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

import aiohttp
from aresponses import ResponsesMockServer
import pytest

from aionotion import async_get_client_with_credentials
from tests.common import TEST_EMAIL, TEST_PASSWORD, TEST_USER_UUID


@pytest.mark.asyncio
async def test_user_info(
    authenticated_notion_api_server: ResponsesMockServer,
    user_info_response: dict[str, Any],
) -> None:
    """Test getting user preferences.

    Args:
    ----
        authenticated_notion_api_server: A mock authenticated Notion API server
        user_info_response: A fixture for a user information response payload.

    """
    async with authenticated_notion_api_server:
        authenticated_notion_api_server.add(
            "api.getnotion.com",
            f"/api/users/{TEST_USER_UUID}",
            "get",
            response=aiohttp.web_response.json_response(user_info_response, status=200),
        )

        async with aiohttp.ClientSession() as session:
            client = await async_get_client_with_credentials(
                TEST_EMAIL, TEST_PASSWORD, session=session
            )
            user_info = await client.user.async_info()
            assert user_info.id == 12345
            assert user_info.uuid == "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
            assert user_info.first_name == "The"
            assert user_info.last_name == "Person"
            assert user_info.email == "user@email.com"
            assert user_info.phone_number is None
            assert user_info.role == "user"
            assert user_info.organization == "Notion User"
            assert user_info.created_at == datetime(
                2019, 4, 30, 1, 35, 3, 781000, tzinfo=timezone.utc
            )
            assert user_info.updated_at == datetime(
                2023, 12, 21, 4, 13, 53, 48000, tzinfo=timezone.utc
            )


@pytest.mark.asyncio
async def test_user_preferences(
    authenticated_notion_api_server: ResponsesMockServer,
    user_preferences_response: dict[str, Any],
) -> None:
    """Test getting user preferences.

    Args:
    ----
        authenticated_notion_api_server: A mock authenticated Notion API server
        user_preferences_response: A fixture for a user preferences response payload.

    """
    async with authenticated_notion_api_server:
        authenticated_notion_api_server.add(
            "api.getnotion.com",
            f"/api/users/{TEST_USER_UUID}/user_preferences",
            "get",
            response=aiohttp.web_response.json_response(
                user_preferences_response, status=200
            ),
        )

        async with aiohttp.ClientSession() as session:
            client = await async_get_client_with_credentials(
                TEST_EMAIL, TEST_PASSWORD, session=session
            )
            user_preferences = await client.user.async_preferences()
            assert user_preferences.user_id == 12345
            assert user_preferences.military_time_enabled is False
            assert user_preferences.celsius_enabled is False
            assert user_preferences.disconnect_alerts_enabled is True
            assert user_preferences.home_away_alerts_enabled is False
            assert user_preferences.battery_alerts_enabled is True
