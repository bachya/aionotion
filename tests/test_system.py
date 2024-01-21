"""Define tests for systems."""
from __future__ import annotations

import json
from datetime import datetime, timezone

import aiohttp
import pytest
from aresponses import ResponsesMockServer

from aionotion import async_get_client

from .common import TEST_EMAIL, TEST_PASSWORD, load_fixture


@pytest.mark.asyncio
async def test_system_all(
    aresponses: ResponsesMockServer,
    authenticated_notion_api_server: ResponsesMockServer,
) -> None:
    """Test getting all systems.

    Args:
        aresponses: An aresponses server.
        authenticated_notion_api_server: A mock authenticated Notion API server
    """
    async with authenticated_notion_api_server:
        authenticated_notion_api_server.add(
            "api.getnotion.com",
            "/api/systems",
            "get",
            response=aiohttp.web_response.json_response(
                json.loads(load_fixture("system_all_response.json")), status=200
            ),
        )

        async with aiohttp.ClientSession() as session:
            client = await async_get_client(TEST_EMAIL, TEST_PASSWORD, session=session)
            response = await client.system.async_all()
            assert len(response.systems) == 1

            assert response.systems[0].uuid == "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
            assert response.systems[0].name == "Home"
            assert response.systems[0].mode == "home"
            assert response.systems[0].partners == []
            assert response.systems[0].latitude == 89.0
            assert response.systems[0].longitude == -170.0
            assert response.systems[0].timezone_id == "Some/Timezone"
            assert response.systems[0].created_at == datetime(
                2019, 4, 30, 1, 35, 21, 870000, tzinfo=timezone.utc
            )
            assert response.systems[0].updated_at == datetime(
                2019, 7, 9, 4, 57, 1, 68000, tzinfo=timezone.utc
            )
            assert response.systems[0].night_time_start == datetime(
                2019, 5, 1, 4, 0, tzinfo=timezone.utc
            )
            assert response.systems[0].night_time_end == datetime(
                2019, 5, 1, 13, 0, tzinfo=timezone.utc
            )
            assert response.systems[0].id == 12345
            assert response.systems[0].locality == "Moon"
            assert response.systems[0].postal_code == "11111"
            assert response.systems[0].administrative_area == "Moon"
            assert response.systems[0].fire_number == "(123) 456-7890"
            assert response.systems[0].police_number == "(123) 456-7890"
            assert response.systems[0].emergency_number == "(123) 456-7890"
            assert response.systems[0].address is None
            assert response.systems[0].notion_pro_permit is None

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_system_get(
    aresponses: ResponsesMockServer,
    authenticated_notion_api_server: ResponsesMockServer,
) -> None:
    """Test getting a system by ID.

    Args:
        aresponses: An aresponses server.
        authenticated_notion_api_server: A mock authenticated Notion API server
    """
    async with authenticated_notion_api_server:
        authenticated_notion_api_server.add(
            "api.getnotion.com",
            "/api/systems/12345",
            "get",
            response=aiohttp.web_response.json_response(
                json.loads(load_fixture("system_get_response.json")), status=200
            ),
        )

        async with aiohttp.ClientSession() as session:
            client = await async_get_client(TEST_EMAIL, TEST_PASSWORD, session=session)
            response = await client.system.async_get(12345)
            assert response.system.uuid == "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
            assert response.system.name == "Home"
            assert response.system.mode == "home"
            assert response.system.partners == []
            assert response.system.latitude == 89.0
            assert response.system.longitude == -170.0
            assert response.system.timezone_id == "Some/Timezone"
            assert response.system.created_at == datetime(
                2019, 4, 30, 1, 35, 21, 870000, tzinfo=timezone.utc
            )
            assert response.system.updated_at == datetime(
                2019, 7, 9, 4, 57, 1, 68000, tzinfo=timezone.utc
            )
            assert response.system.night_time_start == datetime(
                2019, 5, 1, 4, 0, tzinfo=timezone.utc
            )
            assert response.system.night_time_end == datetime(
                2019, 5, 1, 13, 0, tzinfo=timezone.utc
            )
            assert response.system.id == 12345
            assert response.system.locality == "Moon"
            assert response.system.postal_code == "11111"
            assert response.system.administrative_area == "Moon"
            assert response.system.fire_number == "(123) 456-7890"
            assert response.system.police_number == "(123) 456-7890"
            assert response.system.emergency_number == "(123) 456-7890"
            assert response.system.address is None
            assert response.system.notion_pro_permit is None

    aresponses.assert_plan_strictly_followed()
