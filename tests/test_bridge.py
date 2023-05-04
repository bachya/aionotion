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
            bridges = await client.bridge.async_all()
            assert len(bridges) == 2

            assert bridges[0].id == 12345
            assert bridges[0].name is None
            assert bridges[0].mode == "home"
            assert bridges[0].hardware_id == "0x0000000000000000"
            assert bridges[0].hardware_revision == 4
            assert bridges[0].firmware_version.silabs == "1.1.2"
            assert bridges[0].firmware_version.wifi == "0.121.0"
            assert bridges[0].firmware_version.wifi_app == "3.3.0"
            assert bridges[0].missing_at is None
            assert bridges[0].created_at == datetime(
                2019, 6, 27, 0, 18, 44, 337000, tzinfo=timezone.utc
            )
            assert bridges[0].updated_at == datetime(
                2023, 3, 19, 3, 20, 16, 61000, tzinfo=timezone.utc
            )
            assert bridges[0].system_id == 11111
            assert bridges[0].firmware.silabs == "1.1.2"
            assert bridges[0].firmware.wifi == "0.121.0"
            assert bridges[0].firmware.wifi_app == "3.3.0"
            assert bridges[0].links["system"] == 11111

            assert bridges[1].id == 67890
            assert bridges[1].name == "Bridge 2"
            assert bridges[1].mode == "home"
            assert bridges[1].hardware_id == "0x0000000000000000"
            assert bridges[1].hardware_revision == 4
            assert bridges[1].firmware_version.silabs == "1.1.2"
            assert bridges[1].firmware_version.wifi == "0.121.0"
            assert bridges[1].firmware_version.wifi_app == "3.3.0"
            assert bridges[1].missing_at is None
            assert bridges[1].created_at == datetime(
                2019, 4, 30, 1, 43, 50, 497000, tzinfo=timezone.utc
            )
            assert bridges[1].updated_at == datetime(
                2023, 1, 2, 19, 9, 58, 251000, tzinfo=timezone.utc
            )
            assert bridges[1].system_id == 11111
            assert bridges[1].firmware.silabs == "1.1.2"
            assert bridges[1].firmware.wifi == "0.121.0"
            assert bridges[1].firmware.wifi_app == "3.3.0"
            assert bridges[1].links["system"] == 11111

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_bridge_create(
    aresponses: ResponsesMockServer,
    authenticated_notion_api_server: ResponsesMockServer,
    bridge_create_response: dict[str, Any],
) -> None:
    """Test creating a bridge.

    Args:
        aresponses: An aresponses server.
        authenticated_notion_api_server: A mock authenticated Notion API server
        bridge_create_response: An API response payload
    """
    async with authenticated_notion_api_server:
        authenticated_notion_api_server.add(
            "api.getnotion.com",
            "/api/base_stations",
            "post",
            response=aiohttp.web_response.json_response(
                bridge_create_response, status=200
            ),
        )

        async with aiohttp.ClientSession() as session:
            client = await async_get_client(TEST_EMAIL, TEST_PASSWORD, session=session)
            bridge = await client.bridge.async_create(
                {"name": "New Bridge", "system_id": 98765}
            )
            assert bridge.id == 98765
            assert bridge.name == "New Bridge"
            assert bridge.mode == "home"
            assert bridge.hardware_id == "0x0000000000000000"
            assert bridge.hardware_revision == 4
            assert bridge.firmware_version.silabs == "1.1.2"
            assert bridge.firmware_version.wifi == "0.121.0"
            assert bridge.firmware_version.wifi_app == "3.3.0"
            assert bridge.missing_at is None
            assert bridge.created_at == datetime(
                2019, 4, 30, 1, 43, 50, 497000, tzinfo=timezone.utc
            )
            assert bridge.updated_at == datetime(
                2023, 1, 2, 19, 9, 58, 251000, tzinfo=timezone.utc
            )
            assert bridge.system_id == 11111
            assert bridge.firmware.silabs == "1.1.2"
            assert bridge.firmware.wifi == "0.121.0"
            assert bridge.firmware.wifi_app == "3.3.0"
            assert bridge.links["system"] == 11111

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_bridge_delete(
    aresponses: ResponsesMockServer,
    authenticated_notion_api_server: ResponsesMockServer,
) -> None:
    """Test deleting a bridge.

    Args:
        aresponses: An aresponses server.
        authenticated_notion_api_server: A mock authenticated Notion API server
    """
    async with authenticated_notion_api_server:
        authenticated_notion_api_server.add(
            "api.getnotion.com",
            "/api/base_stations/12345",
            "delete",
            aresponses.Response(
                text=None,
                status=200,
                headers={"Content-Type": "application/json; charset=utf-8"},
            ),
        )

        async with aiohttp.ClientSession() as session:
            client = await async_get_client(TEST_EMAIL, TEST_PASSWORD, session=session)
            await client.bridge.async_delete(12345)

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
            "/api/base_stations/98765",
            "get",
            response=aiohttp.web_response.json_response(
                bridge_get_response, status=200
            ),
        )

        async with aiohttp.ClientSession() as session:
            client = await async_get_client(TEST_EMAIL, TEST_PASSWORD, session=session)
            bridge = await client.bridge.async_get(98765)
            assert bridge.id == 98765
            assert bridge.name == "Bridge 1"
            assert bridge.mode == "home"
            assert bridge.hardware_id == "0x0000000000000000"
            assert bridge.hardware_revision == 4
            assert bridge.firmware_version.silabs == "1.1.2"
            assert bridge.firmware_version.wifi == "0.121.0"
            assert bridge.firmware_version.wifi_app == "3.3.0"
            assert bridge.missing_at is None
            assert bridge.created_at == datetime(
                2019, 4, 30, 1, 43, 50, 497000, tzinfo=timezone.utc
            )
            assert bridge.updated_at == datetime(
                2023, 1, 2, 19, 9, 58, 251000, tzinfo=timezone.utc
            )
            assert bridge.system_id == 11111
            assert bridge.firmware.silabs == "1.1.2"
            assert bridge.firmware.wifi == "0.121.0"
            assert bridge.firmware.wifi_app == "3.3.0"
            assert bridge.links["system"] == 11111

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_bridge_reset(
    aresponses: ResponsesMockServer,
    authenticated_notion_api_server: ResponsesMockServer,
    bridge_reset_response: dict[str, Any],
) -> None:
    """Test deleting a bridge.

    Args:
        aresponses: An aresponses server.
        authenticated_notion_api_server: A mock authenticated Notion API server
        bridge_reset_response: An API response payload
    """
    async with authenticated_notion_api_server:
        authenticated_notion_api_server.add(
            "api.getnotion.com",
            "/api/base_stations/98765/reset",
            "put",
            response=aiohttp.web_response.json_response(
                bridge_reset_response, status=200
            ),
        )

        async with aiohttp.ClientSession() as session:
            client = await async_get_client(TEST_EMAIL, TEST_PASSWORD, session=session)
            bridge = await client.bridge.async_reset(98765)
            assert bridge.id == 98765
            assert bridge.name == "Bridge 1"
            assert bridge.mode == "home"
            assert bridge.hardware_id == "0x0000000000000000"
            assert bridge.hardware_revision == 4
            assert bridge.firmware_version.silabs == "1.1.2"
            assert bridge.firmware_version.wifi == "0.121.0"
            assert bridge.firmware_version.wifi_app == "3.3.0"
            assert bridge.missing_at is None
            assert bridge.created_at == datetime(
                2019, 4, 30, 1, 43, 50, 497000, tzinfo=timezone.utc
            )
            assert bridge.updated_at == datetime(
                2023, 1, 2, 19, 9, 58, 251000, tzinfo=timezone.utc
            )
            assert bridge.system_id == 11111
            assert bridge.firmware.silabs == "1.1.2"
            assert bridge.firmware.wifi == "0.121.0"
            assert bridge.firmware.wifi_app == "3.3.0"
            assert bridge.links["system"] == 11111

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_bridge_update(
    aresponses: ResponsesMockServer,
    authenticated_notion_api_server: ResponsesMockServer,
    bridge_update_response: dict[str, Any],
) -> None:
    """Test deleting a bridge.

    Args:
        aresponses: An aresponses server.
        authenticated_notion_api_server: A mock authenticated Notion API server
        bridge_update_response: An API response payload
    """
    async with authenticated_notion_api_server:
        authenticated_notion_api_server.add(
            "api.getnotion.com",
            "/api/base_stations/98765",
            "put",
            response=aiohttp.web_response.json_response(
                bridge_update_response, status=200
            ),
        )

        async with aiohttp.ClientSession() as session:
            client = await async_get_client(TEST_EMAIL, TEST_PASSWORD, session=session)
            bridge = await client.bridge.async_update(
                98765, {"name": "My Updated Name"}
            )
            assert bridge.id == 98765
            assert bridge.name == "My Updated Name"
            assert bridge.mode == "home"
            assert bridge.hardware_id == "0x0000000000000000"
            assert bridge.hardware_revision == 4
            assert bridge.firmware_version.silabs == "1.1.2"
            assert bridge.firmware_version.wifi == "0.121.0"
            assert bridge.firmware_version.wifi_app == "3.3.0"
            assert bridge.missing_at is None
            assert bridge.created_at == datetime(
                2019, 4, 30, 1, 43, 50, 497000, tzinfo=timezone.utc
            )
            assert bridge.updated_at == datetime(
                2023, 1, 2, 19, 9, 58, 251000, tzinfo=timezone.utc
            )
            assert bridge.system_id == 11111
            assert bridge.firmware.silabs == "1.1.2"
            assert bridge.firmware.wifi == "0.121.0"
            assert bridge.firmware.wifi_app == "3.3.0"
            assert bridge.links["system"] == 11111

    aresponses.assert_plan_strictly_followed()
