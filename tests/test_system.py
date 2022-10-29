"""Define tests for systems."""
import json

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
            systems = await client.system.async_all()
            assert len(systems) == 1

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_system_create(
    aresponses: ResponsesMockServer,
    authenticated_notion_api_server: ResponsesMockServer,
) -> None:
    """Test creating a system.

    Args:
        aresponses: An aresponses server.
        authenticated_notion_api_server: A mock authenticated Notion API server
    """
    async with authenticated_notion_api_server:
        authenticated_notion_api_server.add(
            "api.getnotion.com",
            "/api/systems",
            "post",
            response=aiohttp.web_response.json_response(
                json.loads(load_fixture("system_create_response.json")), status=200
            ),
        )

        async with aiohttp.ClientSession() as session:
            client = await async_get_client(TEST_EMAIL, TEST_PASSWORD, session=session)
            create_resp = await client.system.async_create(
                {"name": "New System", "id": 12345}
            )
            assert create_resp["id"] == 12345
            assert create_resp["name"] == "New System"

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_system_delete(
    aresponses: ResponsesMockServer,
    authenticated_notion_api_server: ResponsesMockServer,
) -> None:
    """Test deleting a system.

    Args:
        aresponses: An aresponses server.
        authenticated_notion_api_server: A mock authenticated Notion API server
    """
    async with authenticated_notion_api_server:
        authenticated_notion_api_server.add(
            "api.getnotion.com",
            "/api/systems/12345",
            "delete",
            aresponses.Response(
                text=None,
                status=200,
                headers={"Content-Type": "application/json; charset=utf-8"},
            ),
        )

        async with aiohttp.ClientSession() as session:
            client = await async_get_client(TEST_EMAIL, TEST_PASSWORD, session=session)
            await client.system.async_delete(12345)

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
            system = await client.system.async_get(12345)
            assert system["id"] == 12345
            assert system["name"] == "Home"

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_system_update(
    aresponses: ResponsesMockServer,
    authenticated_notion_api_server: ResponsesMockServer,
) -> None:
    """Test deleting a system.

    Args:
        aresponses: An aresponses server.
        authenticated_notion_api_server: A mock authenticated Notion API server
    """
    async with authenticated_notion_api_server:
        authenticated_notion_api_server.add(
            "api.getnotion.com",
            "/api/systems/12345",
            "put",
            response=aiohttp.web_response.json_response(
                json.loads(load_fixture("system_update_response.json")), status=200
            ),
        )

        async with aiohttp.ClientSession() as session:
            client = await async_get_client(TEST_EMAIL, TEST_PASSWORD, session=session)
            reset_resp = await client.system.async_update(
                12345, {"name": "Updated System Name"}
            )
            assert reset_resp["id"] == 12345
            assert reset_resp["name"] == "Updated System Name"

    aresponses.assert_plan_strictly_followed()
