"""Define tests for bridges."""
import aiohttp
import pytest

from aionotion import async_get_client

from .common import TEST_EMAIL, TEST_PASSWORD, load_fixture


@pytest.mark.asyncio
async def test_bridge_all(aresponses):
    """Test getting all bridges."""
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
        "/api/base_stations",
        "get",
        aresponses.Response(text=load_fixture("bridge_all_response.json"), status=200),
    )

    async with aiohttp.ClientSession() as session:
        client = await async_get_client(TEST_EMAIL, TEST_PASSWORD, session=session)
        bridges = await client.bridge.async_all()
        assert len(bridges) == 1


@pytest.mark.asyncio
async def test_bridge_create(aresponses):
    """Test creating a bridge."""
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
        "/api/base_stations",
        "post",
        aresponses.Response(
            text=load_fixture("bridge_create_response.json"), status=200
        ),
    )

    async with aiohttp.ClientSession() as session:
        client = await async_get_client(TEST_EMAIL, TEST_PASSWORD, session=session)
        create_resp = await client.bridge.async_create(
            {"name": "New Bridge", "system_id": 98765}
        )
        assert create_resp["id"] == 98765
        assert create_resp["name"] == "New Bridge"


@pytest.mark.asyncio
async def test_bridge_delete(aresponses):
    """Test deleting a bridge."""
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
        "/api/base_stations/12345",
        "delete",
        aresponses.Response(text=None, status=200),
    )

    async with aiohttp.ClientSession() as session:
        client = await async_get_client(TEST_EMAIL, TEST_PASSWORD, session=session)
        await client.bridge.async_delete(12345)


@pytest.mark.asyncio
async def test_bridge_get(aresponses):
    """Test getting a bridge by ID."""
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
        "/api/base_stations/12345",
        "get",
        aresponses.Response(text=load_fixture("bridge_get_response.json"), status=200),
    )

    async with aiohttp.ClientSession() as session:
        client = await async_get_client(TEST_EMAIL, TEST_PASSWORD, session=session)
        bridge = await client.bridge.async_get(12345)
        assert bridge["id"] == 12345
        assert bridge["name"] == "My Bridge"


@pytest.mark.asyncio
async def test_bridge_reset(aresponses):
    """Test deleting a bridge."""
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
        "/api/base_stations/12345/reset",
        "put",
        aresponses.Response(
            text=load_fixture("bridge_reset_response.json"), status=200
        ),
    )

    async with aiohttp.ClientSession() as session:
        client = await async_get_client(TEST_EMAIL, TEST_PASSWORD, session=session)
        reset_resp = await client.bridge.async_reset(12345)
        assert reset_resp["id"] == 12345
        assert reset_resp["name"] == "My Bridge"


@pytest.mark.asyncio
async def test_bridge_update(aresponses):
    """Test deleting a bridge."""
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
        "/api/base_stations/12345",
        "put",
        aresponses.Response(
            text=load_fixture("bridge_update_response.json"), status=200
        ),
    )

    async with aiohttp.ClientSession() as session:
        client = await async_get_client(TEST_EMAIL, TEST_PASSWORD, session=session)
        reset_resp = await client.bridge.async_update(
            12345, {"name": "My Updated Name"}
        )
        assert reset_resp["id"] == 12345
        assert reset_resp["name"] == "My Updated Name"
