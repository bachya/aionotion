"""Define tests for bridges."""
from __future__ import annotations

import json
from datetime import datetime, timezone

import aiohttp
import pytest
from aresponses import ResponsesMockServer

from aionotion import async_get_client
from tests.common import TEST_EMAIL, TEST_PASSWORD, load_fixture


@pytest.mark.asyncio
async def test_device_all(
    aresponses: ResponsesMockServer,
    authenticated_notion_api_server: ResponsesMockServer,
) -> None:
    """Test getting all devices.

    Args:
        aresponses: An aresponses server.
        authenticated_notion_api_server: A mock authenticated Notion API server
    """
    async with authenticated_notion_api_server:
        authenticated_notion_api_server.add(
            "api.getnotion.com",
            "/api/devices",
            "get",
            response=aiohttp.web_response.json_response(
                json.loads(load_fixture("device_all_response.json")), status=200
            ),
        )

        async with aiohttp.ClientSession() as session:
            client = await async_get_client(TEST_EMAIL, TEST_PASSWORD, session=session)
            devices = await client.device.async_all()
            assert len(devices) == 1

            assert devices[0].id == 12345
            assert devices[0].token == "123456abcde"
            assert devices[0].platform == "ios"
            assert devices[0].endpoint == "arn:aws:sns:us-west-2:307936840629:..."
            assert devices[0].created_at == datetime(
                2019, 6, 17, 0, 57, 9, 937000, tzinfo=timezone.utc
            )
            assert devices[0].updated_at == datetime(
                2019, 6, 17, 0, 57, 9, 937000, tzinfo=timezone.utc
            )

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_device_create(
    aresponses: ResponsesMockServer,
    authenticated_notion_api_server: ResponsesMockServer,
) -> None:
    """Test creating a device.

    Args:
        aresponses: An aresponses server.
        authenticated_notion_api_server: A mock authenticated Notion API server
    """
    async with authenticated_notion_api_server:
        authenticated_notion_api_server.add(
            "api.getnotion.com",
            "/api/devices",
            "post",
            response=aiohttp.web_response.json_response(
                json.loads(load_fixture("device_create_response.json")), status=200
            ),
        )

        async with aiohttp.ClientSession() as session:
            client = await async_get_client(TEST_EMAIL, TEST_PASSWORD, session=session)
            device = await client.device.async_create({"id": 12345})
            assert device.id == 12345
            assert device.token == "123456abcde"
            assert device.platform == "ios"
            assert device.endpoint == "arn:aws:sns:us-west-2:307936840629:..."
            assert device.created_at == datetime(
                2019, 6, 17, 0, 57, 9, 937000, tzinfo=timezone.utc
            )
            assert device.updated_at == datetime(
                2019, 6, 17, 0, 57, 9, 937000, tzinfo=timezone.utc
            )

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_device_delete(
    aresponses: ResponsesMockServer,
    authenticated_notion_api_server: ResponsesMockServer,
) -> None:
    """Test deleting a device.

    Args:
        aresponses: An aresponses server.
        authenticated_notion_api_server: A mock authenticated Notion API server
    """
    async with authenticated_notion_api_server:
        authenticated_notion_api_server.add(
            "api.getnotion.com",
            "/api/devices/12345",
            "delete",
            aresponses.Response(
                text=None,
                status=200,
                headers={"Content-Type": "application/json; charset=utf-8"},
            ),
        )

        async with aiohttp.ClientSession() as session:
            client = await async_get_client(TEST_EMAIL, TEST_PASSWORD, session=session)
            await client.device.async_delete(12345)

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_device_get(
    aresponses: ResponsesMockServer,
    authenticated_notion_api_server: ResponsesMockServer,
) -> None:
    """Test getting a device by ID.

    Args:
        aresponses: An aresponses server.
        authenticated_notion_api_server: A mock authenticated Notion API server
    """
    async with authenticated_notion_api_server:
        authenticated_notion_api_server.add(
            "api.getnotion.com",
            "/api/devices/12345",
            "get",
            response=aiohttp.web_response.json_response(
                json.loads(load_fixture("device_get_response.json")), status=200
            ),
        )

        async with aiohttp.ClientSession() as session:
            client = await async_get_client(TEST_EMAIL, TEST_PASSWORD, session=session)
            device = await client.device.async_get(12345)
            assert device.id == 12345
            assert device.token == "123456abcde"
            assert device.platform == "ios"
            assert device.endpoint == "arn:aws:sns:us-west-2:307936840629:..."
            assert device.created_at == datetime(
                2019, 6, 17, 0, 57, 9, 937000, tzinfo=timezone.utc
            )
            assert device.updated_at == datetime(
                2019, 6, 17, 0, 57, 9, 937000, tzinfo=timezone.utc
            )

    aresponses.assert_plan_strictly_followed()
