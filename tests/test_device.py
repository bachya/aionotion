"""Define tests for bridges."""
import aiohttp
import pytest

from aionotion import async_get_client

from .common import TEST_EMAIL, TEST_PASSWORD, load_fixture


@pytest.mark.asyncio
async def test_device_all(aresponses):
    """Test getting all devices."""
    aresponses.add(
        "api.getnotion.com",
        "/api/users/sign_in",
        "post",
        aresponses.Response(
            text=load_fixture("auth_success_response.json"),
            status=200,
            headers={"Content-Type": "application/json; charset=utf-8"},
        ),
    )
    aresponses.add(
        "api.getnotion.com",
        "/api/devices",
        "get",
        aresponses.Response(
            text=load_fixture("device_all_response.json"),
            status=200,
            headers={"Content-Type": "application/json; charset=utf-8"},
        ),
    )

    async with aiohttp.ClientSession() as session:
        client = await async_get_client(TEST_EMAIL, TEST_PASSWORD, session=session)
        devices = await client.device.async_all()
        assert len(devices) == 1


@pytest.mark.asyncio
async def test_device_create(aresponses):
    """Test creating a device."""
    aresponses.add(
        "api.getnotion.com",
        "/api/users/sign_in",
        "post",
        aresponses.Response(
            text=load_fixture("auth_success_response.json"),
            status=200,
            headers={"Content-Type": "application/json; charset=utf-8"},
        ),
    )
    aresponses.add(
        "api.getnotion.com",
        "/api/devices",
        "post",
        aresponses.Response(
            text=load_fixture("device_create_response.json"),
            status=200,
            headers={"Content-Type": "application/json; charset=utf-8"},
        ),
    )

    async with aiohttp.ClientSession() as session:
        client = await async_get_client(TEST_EMAIL, TEST_PASSWORD, session=session)
        create_resp = await client.device.async_create({"id": 12345})
        assert create_resp["id"] == 12345
        assert create_resp["token"] == "123456abcde"


@pytest.mark.asyncio
async def test_device_delete(aresponses):
    """Test deleting a device."""
    aresponses.add(
        "api.getnotion.com",
        "/api/users/sign_in",
        "post",
        aresponses.Response(
            text=load_fixture("auth_success_response.json"),
            status=200,
            headers={"Content-Type": "application/json; charset=utf-8"},
        ),
    )
    aresponses.add(
        "api.getnotion.com",
        "/api/devices/12345",
        "delete",
        aresponses.Response(text=None, status=200),
    )

    async with aiohttp.ClientSession() as session:
        client = await async_get_client(TEST_EMAIL, TEST_PASSWORD, session=session)
        await client.device.async_delete(12345)


@pytest.mark.asyncio
async def test_device_get(aresponses):
    """Test getting a device by ID."""
    aresponses.add(
        "api.getnotion.com",
        "/api/users/sign_in",
        "post",
        aresponses.Response(
            text=load_fixture("auth_success_response.json"),
            status=200,
            headers={"Content-Type": "application/json; charset=utf-8"},
        ),
    )
    aresponses.add(
        "api.getnotion.com",
        "/api/devices/12345",
        "get",
        aresponses.Response(
            text=load_fixture("device_get_response.json"),
            status=200,
            headers={"Content-Type": "application/json; charset=utf-8"},
        ),
    )

    async with aiohttp.ClientSession() as session:
        client = await async_get_client(TEST_EMAIL, TEST_PASSWORD, session=session)
        device = await client.device.async_get(12345)
        assert device["id"] == 12345
        assert device["token"] == "123456abcde"
