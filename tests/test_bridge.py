"""Define tests for bridges."""
import json

import aiohttp
import pytest
from aresponses import ResponsesMockServer

from aionotion import async_get_client

from .common import TEST_EMAIL, TEST_PASSWORD, load_fixture


@pytest.mark.asyncio
async def test_bridge_all(
    aresponses: ResponsesMockServer,
    authenticated_notion_api_server: ResponsesMockServer,
) -> None:
    """Test getting all bridges.

    Args:
        aresponses: An aresponses server.
        authenticated_notion_api_server: A mock authenticated Notion API server
    """
    async with authenticated_notion_api_server:
        authenticated_notion_api_server.add(
            "api.getnotion.com",
            "/api/base_stations",
            "get",
            response=aiohttp.web_response.json_response(
                json.loads(load_fixture("bridge_all_response.json")), status=200
            ),
        )

        async with aiohttp.ClientSession() as session:
            client = await async_get_client(TEST_EMAIL, TEST_PASSWORD, session=session)
            bridges = await client.bridge.async_all()
            assert len(bridges) == 1

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_bridge_create(
    aresponses: ResponsesMockServer,
    authenticated_notion_api_server: ResponsesMockServer,
) -> None:
    """Test creating a bridge.

    Args:
        aresponses: An aresponses server.
        authenticated_notion_api_server: A mock authenticated Notion API server
    """
    async with authenticated_notion_api_server:
        authenticated_notion_api_server.add(
            "api.getnotion.com",
            "/api/base_stations",
            "post",
            response=aiohttp.web_response.json_response(
                json.loads(load_fixture("bridge_create_response.json")), status=200
            ),
        )

        async with aiohttp.ClientSession() as session:
            client = await async_get_client(TEST_EMAIL, TEST_PASSWORD, session=session)
            create_resp = await client.bridge.async_create(
                {"name": "New Bridge", "system_id": 98765}
            )
            assert create_resp["id"] == 98765
            assert create_resp["name"] == "New Bridge"

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
) -> None:
    """Test getting a bridge by ID.

    Args:
        aresponses: An aresponses server.
        authenticated_notion_api_server: A mock authenticated Notion API server
    """
    async with authenticated_notion_api_server:
        authenticated_notion_api_server.add(
            "api.getnotion.com",
            "/api/base_stations/12345",
            "get",
            response=aiohttp.web_response.json_response(
                json.loads(load_fixture("bridge_get_response.json")), status=200
            ),
        )

        async with aiohttp.ClientSession() as session:
            client = await async_get_client(TEST_EMAIL, TEST_PASSWORD, session=session)
            bridge = await client.bridge.async_get(12345)
            assert bridge["id"] == 12345
            assert bridge["name"] == "My Bridge"

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_bridge_reset(
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
            "/api/base_stations/12345/reset",
            "put",
            response=aiohttp.web_response.json_response(
                json.loads(load_fixture("bridge_reset_response.json")), status=200
            ),
        )

        async with aiohttp.ClientSession() as session:
            client = await async_get_client(TEST_EMAIL, TEST_PASSWORD, session=session)
            reset_resp = await client.bridge.async_reset(12345)
            assert reset_resp["id"] == 12345
            assert reset_resp["name"] == "My Bridge"

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_bridge_update(
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
            "put",
            response=aiohttp.web_response.json_response(
                json.loads(load_fixture("bridge_update_response.json")), status=200
            ),
        )

        async with aiohttp.ClientSession() as session:
            client = await async_get_client(TEST_EMAIL, TEST_PASSWORD, session=session)
            reset_resp = await client.bridge.async_update(
                12345, {"name": "My Updated Name"}
            )
            assert reset_resp["id"] == 12345
            assert reset_resp["name"] == "My Updated Name"

    aresponses.assert_plan_strictly_followed()
