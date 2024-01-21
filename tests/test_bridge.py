"""Define tests for bridges."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

import aiohttp
import pytest
from aresponses import ResponsesMockServer

from aionotion import async_get_client
from tests.common import TEST_EMAIL, TEST_PASSWORD


@pytest.mark.asyncio
async def test_bridge_all(
    aresponses: ResponsesMockServer,
    authenticated_notion_api_server: ResponsesMockServer,
    bridge_all_response: dict[str, Any],
) -> None:
    """Test getting all bridges.

    Args:
        aresponses: An aresponses server.
        authenticated_notion_api_server: A mock authenticated Notion API server
        bridge_all_response: An API response payload
    """
    async with authenticated_notion_api_server:
        authenticated_notion_api_server.add(
            "api.getnotion.com",
            "/api/base_stations",
            "get",
            response=aiohttp.web_response.json_response(
                bridge_all_response, status=200
            ),
        )

        async with aiohttp.ClientSession() as session:
            client = await async_get_client(TEST_EMAIL, TEST_PASSWORD, session=session)
            response = await client.bridge.async_all()
            assert len(response.bridges) == 1
            assert response.bridges[0].id == 12345
            assert response.bridges[0].name == "Laundry Closet"
            assert response.bridges[0].mode == "home"
            assert response.bridges[0].hardware_id == "0x0000000000000000"
            assert response.bridges[0].hardware_revision == 4
            assert response.bridges[0].firmware_version.silabs == "1.1.2"
            assert response.bridges[0].firmware_version.wifi == "0.121.0"
            assert response.bridges[0].firmware_version.wifi_app == "3.3.0"
            assert response.bridges[0].missing_at is None
            assert response.bridges[0].created_at == datetime(
                2019, 4, 30, 1, 43, 50, 497000, tzinfo=timezone.utc
            )
            assert response.bridges[0].updated_at == datetime(
                2023, 12, 12, 22, 33, 1, 73000, tzinfo=timezone.utc
            )
            assert response.bridges[0].system_id == 12345
            assert response.bridges[0].firmware.silabs == "1.1.2"
            assert response.bridges[0].firmware.ti is None
            assert response.bridges[0].firmware.wifi == "0.121.0"
            assert response.bridges[0].firmware.wifi_app == "3.3.0"
            assert response.bridges[0].links["system"] == 12345

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_bridge_get(
    aresponses: ResponsesMockServer,
    authenticated_notion_api_server: ResponsesMockServer,
    bridge_get_response: dict[str, Any],
) -> None:
    """Test getting a bridge by ID.

    Args:
        aresponses: An aresponses server.
        authenticated_notion_api_server: A mock authenticated Notion API server
        bridge_get_response: An API response payload
    """
    async with authenticated_notion_api_server:
        authenticated_notion_api_server.add(
            "api.getnotion.com",
            "/api/base_stations/12345",
            "get",
            response=aiohttp.web_response.json_response(
                bridge_get_response, status=200
            ),
        )

        async with aiohttp.ClientSession() as session:
            client = await async_get_client(TEST_EMAIL, TEST_PASSWORD, session=session)
            response = await client.bridge.async_get(12345)
            assert response.bridge.id == 12345
            assert response.bridge.name == "Laundry Closet"
            assert response.bridge.mode == "home"
            assert response.bridge.hardware_id == "0x0000000000000000"
            assert response.bridge.hardware_revision == 4
            assert response.bridge.firmware_version.silabs == "1.1.2"
            assert response.bridge.firmware_version.wifi == "0.121.0"
            assert response.bridge.firmware_version.wifi_app == "3.3.0"
            assert response.bridge.missing_at is None
            assert response.bridge.created_at == datetime(
                2019, 4, 30, 1, 43, 50, 497000, tzinfo=timezone.utc
            )
            assert response.bridge.updated_at == datetime(
                2023, 12, 12, 22, 33, 1, 73000, tzinfo=timezone.utc
            )
            assert response.bridge.system_id == 12345
            assert response.bridge.firmware.silabs == "1.1.2"
            assert response.bridge.firmware.ti is None
            assert response.bridge.firmware.wifi == "0.121.0"
            assert response.bridge.firmware.wifi_app == "3.3.0"
            assert response.bridge.links["system"] == 12345

    aresponses.assert_plan_strictly_followed()
