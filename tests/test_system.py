"""Define tests for the REST API."""
# pylint: disable=redefined-outer-name, unused-import
import json

import aiohttp
import pytest

from aionotion import async_get_client

from .const import TEST_EMAIL, TEST_PASSWORD
from .fixtures import auth_success_json  # noqa: F401
from .fixtures.system import (  # noqa: F401
    system_all_json,
    system_create_json,
    system_get_json,
    system_update_json,
)


@pytest.mark.asyncio
async def test_system_all(
    aresponses, event_loop, auth_success_json, system_all_json  # noqa: F811
):
    """Test getting all systems."""
    aresponses.add(
        "api.getnotion.com",
        "/api/users/sign_in",
        "post",
        aresponses.Response(text=json.dumps(auth_success_json), status=200),
    )
    aresponses.add(
        "api.getnotion.com",
        "/api/systems",
        "get",
        aresponses.Response(text=json.dumps(system_all_json), status=200),
    )

    async with aiohttp.ClientSession(loop=event_loop) as websession:
        client = await async_get_client(TEST_EMAIL, TEST_PASSWORD, websession)
        systems = await client.system.async_all()

        assert len(systems) == 1


@pytest.mark.asyncio
async def test_system_create(
    aresponses, event_loop, auth_success_json, system_create_json  # noqa: F811
):
    """Test creating a system."""
    aresponses.add(
        "api.getnotion.com",
        "/api/users/sign_in",
        "post",
        aresponses.Response(text=json.dumps(auth_success_json), status=200),
    )
    aresponses.add(
        "api.getnotion.com",
        "/api/systems",
        "post",
        aresponses.Response(text=json.dumps(system_create_json), status=200),
    )

    async with aiohttp.ClientSession(loop=event_loop) as websession:
        client = await async_get_client(TEST_EMAIL, TEST_PASSWORD, websession)
        create_resp = await client.system.async_create(
            {"name": "New System", "id": 12345}
        )

        assert create_resp["id"] == 12345
        assert create_resp["name"] == "New System"


@pytest.mark.asyncio
async def test_system_delete(aresponses, event_loop, auth_success_json):  # noqa: F811
    """Test deleting a system."""
    aresponses.add(
        "api.getnotion.com",
        "/api/users/sign_in",
        "post",
        aresponses.Response(text=json.dumps(auth_success_json), status=200),
    )
    aresponses.add(
        "api.getnotion.com",
        "/api/systems/12345",
        "delete",
        aresponses.Response(text=None, status=200),
    )

    async with aiohttp.ClientSession(loop=event_loop) as websession:
        client = await async_get_client(TEST_EMAIL, TEST_PASSWORD, websession)
        await client.system.async_delete(12345)


@pytest.mark.asyncio
async def test_system_get(
    aresponses, event_loop, auth_success_json, system_get_json  # noqa: F811
):
    """Test getting a system by ID."""
    aresponses.add(
        "api.getnotion.com",
        "/api/users/sign_in",
        "post",
        aresponses.Response(text=json.dumps(auth_success_json), status=200),
    )
    aresponses.add(
        "api.getnotion.com",
        "/api/systems/12345",
        "get",
        aresponses.Response(text=json.dumps(system_get_json), status=200),
    )

    async with aiohttp.ClientSession(loop=event_loop) as websession:
        client = await async_get_client(TEST_EMAIL, TEST_PASSWORD, websession)
        system = await client.system.async_get(12345)

        assert system["id"] == 12345
        assert system["name"] == "Home"


@pytest.mark.asyncio
async def test_system_update(
    aresponses, event_loop, auth_success_json, system_update_json  # noqa: F811
):
    """Test deleting a system."""
    aresponses.add(
        "api.getnotion.com",
        "/api/users/sign_in",
        "post",
        aresponses.Response(text=json.dumps(auth_success_json), status=200),
    )
    aresponses.add(
        "api.getnotion.com",
        "/api/systems/12345",
        "put",
        aresponses.Response(text=json.dumps(system_update_json), status=200),
    )

    async with aiohttp.ClientSession(loop=event_loop) as websession:
        client = await async_get_client(TEST_EMAIL, TEST_PASSWORD, websession)
        reset_resp = await client.system.async_update(
            12345, {"name": "Updated System Name"}
        )

        assert reset_resp["id"] == 12345
        assert reset_resp["name"] == "Updated System Name"
