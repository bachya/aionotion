"""Define tests for systems."""

from __future__ import annotations

from datetime import datetime, timezone

import aiohttp
from aresponses import ResponsesMockServer
import pytest

from aionotion import async_get_client_with_credentials

from .common import TEST_EMAIL, TEST_PASSWORD


@pytest.mark.asyncio()
async def test_system_all(
    aresponses: ResponsesMockServer,
    authenticated_notion_api_server: ResponsesMockServer,
    system_all_response: dict[str, str],
) -> None:
    """Test getting all systems.

    Args:
    ----
        aresponses: An aresponses server.
        authenticated_notion_api_server: A mock authenticated Notion API server
        system_all_response: A fixture for a system all response.

    """
    async with authenticated_notion_api_server:
        authenticated_notion_api_server.add(
            "api.getnotion.com",
            "/api/systems",
            "get",
            response=aiohttp.web_response.json_response(
                system_all_response, status=200
            ),
        )

        async with aiohttp.ClientSession() as session:
            client = await async_get_client_with_credentials(
                TEST_EMAIL, TEST_PASSWORD, session=session
            )
            systems = await client.system.async_all()
            assert len(systems) == 1
            assert systems[0].uuid == "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
            assert systems[0].name == "Home"
            assert systems[0].mode == "home"
            assert systems[0].partners == []
            assert systems[0].latitude == 89.0
            assert systems[0].longitude == -170.0
            assert systems[0].timezone_id == "Some/Timezone"
            assert systems[0].created_at == datetime(
                2019, 4, 30, 1, 35, 21, 870000, tzinfo=timezone.utc
            )
            assert systems[0].updated_at == datetime(
                2019, 7, 9, 4, 57, 1, 68000, tzinfo=timezone.utc
            )
            assert systems[0].night_time_start == datetime(
                2019, 5, 1, 4, 0, tzinfo=timezone.utc
            )
            assert systems[0].night_time_end == datetime(
                2019, 5, 1, 13, 0, tzinfo=timezone.utc
            )
            assert systems[0].id == 12345
            assert systems[0].locality == "Moon"
            assert systems[0].postal_code == "11111"
            assert systems[0].administrative_area == "Moon"
            assert systems[0].fire_number == "(123) 456-7890"
            assert systems[0].police_number == "(123) 456-7890"
            assert systems[0].emergency_number == "(123) 456-7890"
            assert systems[0].address is None
            assert systems[0].notion_pro_permit is None

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio()
async def test_system_get(
    aresponses: ResponsesMockServer,
    authenticated_notion_api_server: ResponsesMockServer,
    system_get_response: dict[str, str],
) -> None:
    """Test getting a system by ID.

    Args:
    ----
        aresponses: An aresponses server.
        authenticated_notion_api_server: A mock authenticated Notion API server
        system_get_response: A fixture for a system get response.

    """
    async with authenticated_notion_api_server:
        authenticated_notion_api_server.add(
            "api.getnotion.com",
            "/api/systems/12345",
            "get",
            response=aiohttp.web_response.json_response(
                system_get_response, status=200
            ),
        )

        async with aiohttp.ClientSession() as session:
            client = await async_get_client_with_credentials(
                TEST_EMAIL, TEST_PASSWORD, session=session
            )
            system = await client.system.async_get(12345)
            assert system.uuid == "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
            assert system.name == "Home"
            assert system.mode == "home"
            assert system.partners == []
            assert system.latitude == 89.0
            assert system.longitude == -170.0
            assert system.timezone_id == "Some/Timezone"
            assert system.created_at == datetime(
                2019, 4, 30, 1, 35, 21, 870000, tzinfo=timezone.utc
            )
            assert system.updated_at == datetime(
                2019, 7, 9, 4, 57, 1, 68000, tzinfo=timezone.utc
            )
            assert system.night_time_start == datetime(
                2019, 5, 1, 4, 0, tzinfo=timezone.utc
            )
            assert system.night_time_end == datetime(
                2019, 5, 1, 13, 0, tzinfo=timezone.utc
            )
            assert system.id == 12345
            assert system.locality == "Moon"
            assert system.postal_code == "11111"
            assert system.administrative_area == "Moon"
            assert system.fire_number == "(123) 456-7890"
            assert system.police_number == "(123) 456-7890"
            assert system.emergency_number == "(123) 456-7890"
            assert system.address is None
            assert system.notion_pro_permit is None

    aresponses.assert_plan_strictly_followed()
