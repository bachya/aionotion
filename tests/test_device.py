"""Define tests for bridges."""
# pylint: disable=redefined-outer-name, unused-import
import json

import aiohttp
import pytest

from aionotion import async_get_client

from .const import TEST_EMAIL, TEST_PASSWORD
from .fixtures import auth_success_json  # noqa: F401
from .fixtures.device import (  # noqa: F401
    device_all_json,
    device_create_json,
    device_get_json,
)


@pytest.mark.asyncio
async def test_device_all(
    aresponses, event_loop, auth_success_json, device_all_json  # noqa: F811
):
    """Test getting all devices."""
    aresponses.add(
        "api.getnotion.com",
        "/api/users/sign_in",
        "post",
        aresponses.Response(text=json.dumps(auth_success_json), status=200),
    )
    aresponses.add(
        "api.getnotion.com",
        "/api/devices",
        "get",
        aresponses.Response(text=json.dumps(device_all_json), status=200),
    )

    async with aiohttp.ClientSession(loop=event_loop) as websession:
        client = await async_get_client(TEST_EMAIL, TEST_PASSWORD, websession)
        devices = await client.device.async_all()

        assert len(devices) == 1


@pytest.mark.asyncio
async def test_device_create(
    aresponses, event_loop, auth_success_json, device_create_json  # noqa: F811
):
    """Test creating a device."""
    aresponses.add(
        "api.getnotion.com",
        "/api/users/sign_in",
        "post",
        aresponses.Response(text=json.dumps(auth_success_json), status=200),
    )
    aresponses.add(
        "api.getnotion.com",
        "/api/devices",
        "post",
        aresponses.Response(text=json.dumps(device_create_json), status=200),
    )

    async with aiohttp.ClientSession(loop=event_loop) as websession:
        client = await async_get_client(TEST_EMAIL, TEST_PASSWORD, websession)
        create_resp = await client.device.async_create({"id": 12345})

        assert create_resp["id"] == 12345
        assert create_resp["token"] == "123456abcde"


@pytest.mark.asyncio
async def test_device_delete(aresponses, event_loop, auth_success_json):  # noqa: F811
    """Test deleting a device."""
    aresponses.add(
        "api.getnotion.com",
        "/api/users/sign_in",
        "post",
        aresponses.Response(text=json.dumps(auth_success_json), status=200),
    )
    aresponses.add(
        "api.getnotion.com",
        "/api/devices/12345",
        "delete",
        aresponses.Response(text=None, status=200),
    )

    async with aiohttp.ClientSession(loop=event_loop) as websession:
        client = await async_get_client(TEST_EMAIL, TEST_PASSWORD, websession)
        await client.device.async_delete(12345)


@pytest.mark.asyncio
async def test_device_get(
    aresponses, event_loop, auth_success_json, device_get_json  # noqa: F811
):
    """Test getting a device by ID."""
    aresponses.add(
        "api.getnotion.com",
        "/api/users/sign_in",
        "post",
        aresponses.Response(text=json.dumps(auth_success_json), status=200),
    )
    aresponses.add(
        "api.getnotion.com",
        "/api/devices/12345",
        "get",
        aresponses.Response(text=json.dumps(device_get_json), status=200),
    )

    async with aiohttp.ClientSession(loop=event_loop) as websession:
        client = await async_get_client(TEST_EMAIL, TEST_PASSWORD, websession)
        device = await client.device.async_get(12345)

        assert device["id"] == 12345
        assert device["token"] == "123456abcde"
