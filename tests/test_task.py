"""Define tests for the REST API."""
# pylint: disable=redefined-outer-name, unused-import
import datetime
import json

import aiohttp
import pytest

from aionotion import async_get_client

from .const import TEST_EMAIL, TEST_PASSWORD
from .fixtures import auth_success_json  # noqa: F401
from .fixtures.task import (  # noqa: F401
    task_all_json,
    task_create_json,
    task_get_json,
    task_history_json,
)


@pytest.mark.asyncio
async def test_task_all(
    aresponses, event_loop, auth_success_json, task_all_json  # noqa: F811
):
    """Test getting all tasks."""
    aresponses.add(
        "api.getnotion.com",
        "/api/users/sign_in",
        "post",
        aresponses.Response(text=json.dumps(auth_success_json), status=200),
    )
    aresponses.add(
        "api.getnotion.com",
        "/api/tasks",
        "get",
        aresponses.Response(text=json.dumps(task_all_json), status=200),
    )

    async with aiohttp.ClientSession(loop=event_loop) as websession:
        client = await async_get_client(TEST_EMAIL, TEST_PASSWORD, websession)
        tasks = await client.task.async_all()

        assert len(tasks) == 7


@pytest.mark.asyncio
async def test_task_create(
    aresponses, event_loop, auth_success_json, task_create_json  # noqa: F811
):
    """Test creating a task."""
    aresponses.add(
        "api.getnotion.com",
        "/api/users/sign_in",
        "post",
        aresponses.Response(text=json.dumps(auth_success_json), status=200),
    )
    aresponses.add(
        "api.getnotion.com",
        "/api/sensors/12345/tasks",
        "post",
        aresponses.Response(text=json.dumps(task_create_json), status=200),
    )

    async with aiohttp.ClientSession(loop=event_loop) as websession:
        client = await async_get_client(TEST_EMAIL, TEST_PASSWORD, websession)
        create_resp = await client.task.async_create(
            12345, [{"id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", "type": "missing"}]
        )

        assert create_resp["id"] == "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
        assert create_resp["task_type"] == "missing"


@pytest.mark.asyncio
async def test_task_delete(aresponses, event_loop, auth_success_json):  # noqa: F811
    """Test deleting a task."""
    aresponses.add(
        "api.getnotion.com",
        "/api/users/sign_in",
        "post",
        aresponses.Response(text=json.dumps(auth_success_json), status=200),
    )
    aresponses.add(
        "api.getnotion.com",
        "/api/sensors/12345/tasks/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
        "delete",
        aresponses.Response(text=None, status=200),
    )

    async with aiohttp.ClientSession(loop=event_loop) as websession:
        client = await async_get_client(TEST_EMAIL, TEST_PASSWORD, websession)
        await client.task.async_delete(12345, "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx")


@pytest.mark.asyncio
async def test_task_get(
    aresponses, event_loop, auth_success_json, task_get_json  # noqa: F811
):
    """Test getting a task by ID."""
    aresponses.add(
        "api.getnotion.com",
        "/api/users/sign_in",
        "post",
        aresponses.Response(text=json.dumps(auth_success_json), status=200),
    )
    aresponses.add(
        "api.getnotion.com",
        "/api/tasks/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
        "get",
        aresponses.Response(text=json.dumps(task_get_json), status=200),
    )

    async with aiohttp.ClientSession(loop=event_loop) as websession:
        client = await async_get_client(TEST_EMAIL, TEST_PASSWORD, websession)
        task = await client.task.async_get("xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx")

        assert task["id"] == "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
        assert task["task_type"] == "missing"


@pytest.mark.asyncio
async def test_task_history(
    aresponses, event_loop, auth_success_json, task_history_json  # noqa: F811
):
    """Test getting a task's history."""
    aresponses.add(
        "api.getnotion.com",
        "/api/users/sign_in",
        "post",
        aresponses.Response(text=json.dumps(auth_success_json), status=200),
    )
    aresponses.add(
        "api.getnotion.com",
        "/api/tasks/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/data",
        "get",
        aresponses.Response(text=json.dumps(task_history_json), status=200),
    )

    async with aiohttp.ClientSession(loop=event_loop) as websession:
        client = await async_get_client(TEST_EMAIL, TEST_PASSWORD, websession)
        history = await client.task.async_history(
            "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
            data_before=datetime.datetime.now(),
            data_after=datetime.datetime.now() - datetime.timedelta(days=3),
        )

        assert len(history) == 3
