"""Define tests for the REST API."""
import datetime

import aiohttp
import pytest

from aionotion import async_get_client

from .common import TEST_EMAIL, TEST_PASSWORD, load_fixture


@pytest.mark.asyncio
async def test_task_all(aresponses):
    """Test getting all tasks."""
    aresponses.add(
        "api.getnotion.com",
        "/api/users/sign_in",
        "post",
        aresponses.Response(
            text=load_fixture("auth_success_response.json"), status=200
        ),
    )
    aresponses.add(
        "api.getnotion.com",
        "/api/tasks",
        "get",
        aresponses.Response(text=load_fixture("task_all_response.json"), status=200),
    )

    async with aiohttp.ClientSession() as session:
        client = await async_get_client(TEST_EMAIL, TEST_PASSWORD, session=session)
        tasks = await client.task.async_all()
        assert len(tasks) == 4
        assert tasks[0]["status"]["value"] == "not_missing"
        assert tasks[1]["status"]["insights"]["primary"]["to_state"] == "no_leak"


@pytest.mark.asyncio
async def test_task_create(aresponses):
    """Test creating a task."""
    aresponses.add(
        "api.getnotion.com",
        "/api/users/sign_in",
        "post",
        aresponses.Response(
            text=load_fixture("auth_success_response.json"), status=200
        ),
    )
    aresponses.add(
        "api.getnotion.com",
        "/api/sensors/12345/tasks",
        "post",
        aresponses.Response(text=load_fixture("task_create_response.json"), status=200),
    )

    async with aiohttp.ClientSession() as session:
        client = await async_get_client(TEST_EMAIL, TEST_PASSWORD, session=session)
        create_resp = await client.task.async_create(
            12345, [{"id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", "type": "missing"}]
        )
        assert create_resp["id"] == "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
        assert create_resp["task_type"] == "missing"


@pytest.mark.asyncio
async def test_task_delete(aresponses):
    """Test deleting a task."""
    aresponses.add(
        "api.getnotion.com",
        "/api/users/sign_in",
        "post",
        aresponses.Response(
            text=load_fixture("auth_success_response.json"), status=200
        ),
    )
    aresponses.add(
        "api.getnotion.com",
        "/api/sensors/12345/tasks/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
        "delete",
        aresponses.Response(text=None, status=200),
    )

    async with aiohttp.ClientSession() as session:
        client = await async_get_client(TEST_EMAIL, TEST_PASSWORD, session=session)
        await client.task.async_delete(12345, "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx")


@pytest.mark.asyncio
async def test_task_get(aresponses):
    """Test getting a task by ID."""
    aresponses.add(
        "api.getnotion.com",
        "/api/users/sign_in",
        "post",
        aresponses.Response(
            text=load_fixture("auth_success_response.json"), status=200
        ),
    )
    aresponses.add(
        "api.getnotion.com",
        "/api/tasks/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
        "get",
        aresponses.Response(text=load_fixture("task_get_response.json"), status=200),
    )

    async with aiohttp.ClientSession() as session:
        client = await async_get_client(TEST_EMAIL, TEST_PASSWORD, session=session)
        task = await client.task.async_get("xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx")
        assert task["id"] == "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
        assert task["task_type"] == "missing"


@pytest.mark.asyncio
async def test_task_history(aresponses):
    """Test getting a task's history."""
    aresponses.add(
        "api.getnotion.com",
        "/api/users/sign_in",
        "post",
        aresponses.Response(
            text=load_fixture("auth_success_response.json"), status=200
        ),
    )
    aresponses.add(
        "api.getnotion.com",
        "/api/tasks/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/data",
        "get",
        aresponses.Response(
            text=load_fixture("task_history_response.json"), status=200
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
