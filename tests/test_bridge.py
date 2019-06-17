"""Define tests for bridges."""
# pylint: disable=redefined-outer-name, unused-import
import json

import aiohttp
import pytest

from aionotion import async_get_client

from .const import TEST_EMAIL, TEST_PASSWORD
from .fixtures import auth_success_json  # noqa: F401
from .fixtures.bridge import (  # noqa: F401
    bridge_all_json,
    bridge_create_json,
    bridge_delete_json,
    bridge_get_json,
    bridge_reset_json,
    bridge_update_json,
)


@pytest.mark.asyncio
async def test_bridge_all(
    aresponses, event_loop, auth_success_json, bridge_all_json  # noqa: F811
):
    """Test getting all bridges."""
    aresponses.add(
        "api.getnotion.com",
        "/api/users/sign_in",
        "post",
        aresponses.Response(text=json.dumps(auth_success_json), status=200),
    )
    aresponses.add(
        "api.getnotion.com",
        "/api/base_stations",
        "get",
        aresponses.Response(text=json.dumps(bridge_all_json), status=200),
    )

    async with aiohttp.ClientSession(loop=event_loop) as websession:
        client = await async_get_client(TEST_EMAIL, TEST_PASSWORD, websession)
        bridges = await client.bridge.async_all()

        assert len(bridges) == 1


@pytest.mark.asyncio
async def test_bridge_create(
    aresponses, event_loop, auth_success_json, bridge_create_json  # noqa: F811
):
    """Test creating a bridge."""
    aresponses.add(
        "api.getnotion.com",
        "/api/users/sign_in",
        "post",
        aresponses.Response(text=json.dumps(auth_success_json), status=200),
    )
    aresponses.add(
        "api.getnotion.com",
        "/api/base_stations",
        "post",
        aresponses.Response(text=json.dumps(bridge_create_json), status=200),
    )

    async with aiohttp.ClientSession(loop=event_loop) as websession:
        client = await async_get_client(TEST_EMAIL, TEST_PASSWORD, websession)
        create_resp = await client.bridge.async_create(
            {"name": "New Bridge", "system_id": 98765}
        )

        assert len(create_resp) == 2
        assert create_resp[1]["id"] == 98765
        assert create_resp[1]["name"] == "New Bridge"


@pytest.mark.asyncio
async def test_bridge_delete(
    aresponses, event_loop, auth_success_json, bridge_delete_json  # noqa: F811
):
    """Test deleting a bridge."""
    aresponses.add(
        "api.getnotion.com",
        "/api/users/sign_in",
        "post",
        aresponses.Response(text=json.dumps(auth_success_json), status=200),
    )
    aresponses.add(
        "api.getnotion.com",
        "/api/base_stations/12345",
        "delete",
        aresponses.Response(text=json.dumps(bridge_delete_json), status=200),
    )

    async with aiohttp.ClientSession(loop=event_loop) as websession:
        client = await async_get_client(TEST_EMAIL, TEST_PASSWORD, websession)
        delete_resp = await client.bridge.async_delete(12345)

        assert not delete_resp


@pytest.mark.asyncio
async def test_bridge_get(
    aresponses, event_loop, auth_success_json, bridge_get_json  # noqa: F811
):
    """Test getting a bridge by ID."""
    aresponses.add(
        "api.getnotion.com",
        "/api/users/sign_in",
        "post",
        aresponses.Response(text=json.dumps(auth_success_json), status=200),
    )
    aresponses.add(
        "api.getnotion.com",
        "/api/base_stations/12345",
        "get",
        aresponses.Response(text=json.dumps(bridge_get_json), status=200),
    )

    async with aiohttp.ClientSession(loop=event_loop) as websession:
        client = await async_get_client(TEST_EMAIL, TEST_PASSWORD, websession)
        bridge = await client.bridge.async_get(12345)

        assert bridge["id"] == 12345
        assert bridge["name"] == "My Bridge"


@pytest.mark.asyncio
async def test_bridge_reset(
    aresponses, event_loop, auth_success_json, bridge_reset_json  # noqa: F811
):
    """Test deleting a bridge."""
    aresponses.add(
        "api.getnotion.com",
        "/api/users/sign_in",
        "post",
        aresponses.Response(text=json.dumps(auth_success_json), status=200),
    )
    aresponses.add(
        "api.getnotion.com",
        "/api/base_stations/12345/reset",
        "put",
        aresponses.Response(text=json.dumps(bridge_reset_json), status=200),
    )

    async with aiohttp.ClientSession(loop=event_loop) as websession:
        client = await async_get_client(TEST_EMAIL, TEST_PASSWORD, websession)
        reset_resp = await client.bridge.async_reset(12345)

        assert reset_resp["id"] == 12345
        assert reset_resp["name"] == "My Bridge"


@pytest.mark.asyncio
async def test_bridge_update(
    aresponses, event_loop, auth_success_json, bridge_update_json  # noqa: F811
):
    """Test deleting a bridge."""
    aresponses.add(
        "api.getnotion.com",
        "/api/users/sign_in",
        "post",
        aresponses.Response(text=json.dumps(auth_success_json), status=200),
    )
    aresponses.add(
        "api.getnotion.com",
        "/api/base_stations/12345",
        "put",
        aresponses.Response(text=json.dumps(bridge_update_json), status=200),
    )

    async with aiohttp.ClientSession(loop=event_loop) as websession:
        client = await async_get_client(TEST_EMAIL, TEST_PASSWORD, websession)
        reset_resp = await client.bridge.async_update(
            12345, {"name": "My Updated Name"}
        )

        assert reset_resp["id"] == 12345
        assert reset_resp["name"] == "My Updated Name"
