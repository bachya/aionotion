"""Define tests for the REST API."""
import datetime
import json

import aiohttp
import pytest
from aresponses import ResponsesMockServer

from aionotion import async_get_client

from .common import TEST_EMAIL, TEST_PASSWORD, load_fixture


@pytest.mark.asyncio
async def test_task_all(
    aresponses: ResponsesMockServer,
    authenticated_notion_api_server: ResponsesMockServer,
) -> None:
    """Test getting all tasks.

    Args:
        aresponses: An aresponses server.
        authenticated_notion_api_server: A mock authenticated Notion API server
    """
    async with authenticated_notion_api_server:
        authenticated_notion_api_server.add(
            "api.getnotion.com",
            "/api/tasks",
            "get",
            response=aiohttp.web_response.json_response(
                json.loads(load_fixture("task_all_response.json")), status=200
            ),
        )

        async with aiohttp.ClientSession() as session:
            client = await async_get_client(TEST_EMAIL, TEST_PASSWORD, session=session)
            tasks = await client.task.async_all()
            assert len(tasks) == 4
            assert tasks[0]["status"]["value"] == "not_missing"
            assert tasks[1]["status"]["insights"]["primary"]["to_state"] == "no_leak"

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_task_create(
    aresponses: ResponsesMockServer,
    authenticated_notion_api_server: ResponsesMockServer,
) -> None:
    """Test creating a task.

    Args:
        aresponses: An aresponses server.
        authenticated_notion_api_server: A mock authenticated Notion API server
    """
    async with authenticated_notion_api_server:
        authenticated_notion_api_server.add(
            "api.getnotion.com",
            "/api/sensors/12345/tasks",
            "post",
            response=aiohttp.web_response.json_response(
                json.loads(load_fixture("task_create_response.json")), status=200
            ),
        )

        async with aiohttp.ClientSession() as session:
            client = await async_get_client(TEST_EMAIL, TEST_PASSWORD, session=session)
            create_resp = await client.task.async_create(
                12345,
                [{"id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", "type": "missing"}],
            )
            assert create_resp["id"] == "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
            assert create_resp["task_type"] == "missing"

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_task_delete(
    aresponses: ResponsesMockServer,
    authenticated_notion_api_server: ResponsesMockServer,
) -> None:
    """Test deleting a task.

    Args:
        aresponses: An aresponses server.
        authenticated_notion_api_server: A mock authenticated Notion API server
    """
    async with authenticated_notion_api_server:
        authenticated_notion_api_server.add(
            "api.getnotion.com",
            "/api/sensors/12345/tasks/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
            "delete",
            aresponses.Response(
                text=None,
                status=200,
                headers={"Content-Type": "application/json; charset=utf-8"},
            ),
        )

        async with aiohttp.ClientSession() as session:
            client = await async_get_client(TEST_EMAIL, TEST_PASSWORD, session=session)
            await client.task.async_delete(
                12345, "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
            )

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_task_get(
    aresponses: ResponsesMockServer,
    authenticated_notion_api_server: ResponsesMockServer,
) -> None:
    """Test getting a task by ID.

    Args:
        aresponses: An aresponses server.
        authenticated_notion_api_server: A mock authenticated Notion API server
    """
    async with authenticated_notion_api_server:
        authenticated_notion_api_server.add(
            "api.getnotion.com",
            "/api/tasks/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
            "get",
            response=aiohttp.web_response.json_response(
                json.loads(load_fixture("task_get_response.json")), status=200
            ),
        )

        async with aiohttp.ClientSession() as session:
            client = await async_get_client(TEST_EMAIL, TEST_PASSWORD, session=session)
            task = await client.task.async_get("xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx")
            assert task["id"] == "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
            assert task["task_type"] == "missing"

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_task_history(
    aresponses: ResponsesMockServer,
    authenticated_notion_api_server: ResponsesMockServer,
) -> None:
    """Test getting a task's history.

    Args:
        aresponses: An aresponses server.
        authenticated_notion_api_server: A mock authenticated Notion API server
    """
    async with authenticated_notion_api_server:
        authenticated_notion_api_server.add(
            "api.getnotion.com",
            "/api/tasks/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/data",
            "get",
            response=aiohttp.web_response.json_response(
                json.loads(load_fixture("task_history_response.json")), status=200
            ),
        )

        async with aiohttp.ClientSession() as session:
            client = await async_get_client(TEST_EMAIL, TEST_PASSWORD, session=session)
            history = await client.task.async_history(
                "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
                data_before=datetime.datetime.now(),
                data_after=datetime.datetime.now() - datetime.timedelta(days=3),
            )
            assert len(history) == 3

    aresponses.assert_plan_strictly_followed()
