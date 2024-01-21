"""Define tests for users."""
from __future__ import annotations

import json

import aiohttp
import pytest
from aresponses import ResponsesMockServer

from aionotion import async_get_client
from tests.common import TEST_EMAIL, TEST_PASSWORD, load_fixture


@pytest.mark.asyncio
async def test_user_preferences(
    authenticated_notion_api_server: ResponsesMockServer,
) -> None:
    """Test getting user preferences.

    Args:
        authenticated_notion_api_server: A mock authenticated Notion API server
    """
    async with authenticated_notion_api_server:
        authenticated_notion_api_server.add(
            "api.getnotion.com",
            "/api/users/12345/user_preferences",
            "get",
            response=aiohttp.web_response.json_response(
                json.loads(load_fixture("user_preferences_response.json")), status=200
            ),
        )

        async with aiohttp.ClientSession() as session:
            client = await async_get_client(TEST_EMAIL, TEST_PASSWORD, session=session)
            response = await client.user.async_preferences()
            assert response.user_preferences.user_id == 12345
            assert response.user_preferences.military_time_enabled is False
            assert response.user_preferences.celsius_enabled is False
            assert response.user_preferences.disconnect_alerts_enabled is True
            assert response.user_preferences.home_away_alerts_enabled is False
            assert response.user_preferences.battery_alerts_enabled is True
