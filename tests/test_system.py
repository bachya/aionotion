"""Define tests for systems."""
import aiohttp
import pytest

from aionotion import async_get_client

from .common import TEST_EMAIL, TEST_PASSWORD, load_fixture


@pytest.mark.asyncio
async def test_system_all(aresponses):
    """Test getting all systems."""
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
        "/api/systems",
        "get",
        aresponses.Response(
            text=load_fixture("system_all_response.json"),
            status=200,
            headers={"Content-Type": "application/json; charset=utf-8"},
        ),
    )

    async with aiohttp.ClientSession() as session:
        client = await async_get_client(TEST_EMAIL, TEST_PASSWORD, session=session)
        systems = await client.system.async_all()
        assert len(systems) == 1


@pytest.mark.asyncio
async def test_system_create(aresponses):
    """Test creating a system."""
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
        "/api/systems",
        "post",
        aresponses.Response(
            text=load_fixture("system_create_response.json"),
            status=200,
            headers={"Content-Type": "application/json; charset=utf-8"},
        ),
    )

    async with aiohttp.ClientSession() as session:
        client = await async_get_client(TEST_EMAIL, TEST_PASSWORD, session=session)
        create_resp = await client.system.async_create(
            {"name": "New System", "id": 12345}
        )
        assert create_resp["id"] == 12345
        assert create_resp["name"] == "New System"


@pytest.mark.asyncio
async def test_system_delete(aresponses):
    """Test deleting a system."""
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
        "/api/systems/12345",
        "delete",
        aresponses.Response(text=None, status=200),
    )

    async with aiohttp.ClientSession() as session:
        client = await async_get_client(TEST_EMAIL, TEST_PASSWORD, session=session)
        await client.system.async_delete(12345)


@pytest.mark.asyncio
async def test_system_get(aresponses):
    """Test getting a system by ID."""
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
        "/api/systems/12345",
        "get",
        aresponses.Response(
            text=load_fixture("system_get_response.json"),
            status=200,
            headers={"Content-Type": "application/json; charset=utf-8"},
        ),
    )

    async with aiohttp.ClientSession() as session:
        client = await async_get_client(TEST_EMAIL, TEST_PASSWORD, session=session)
        system = await client.system.async_get(12345)
        assert system["id"] == 12345
        assert system["name"] == "Home"


@pytest.mark.asyncio
async def test_system_update(aresponses):
    """Test deleting a system."""
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
        "/api/systems/12345",
        "put",
        aresponses.Response(
            text=load_fixture("system_update_response.json"),
            status=200,
            headers={"Content-Type": "application/json; charset=utf-8"},
        ),
    )

    async with aiohttp.ClientSession() as session:
        client = await async_get_client(TEST_EMAIL, TEST_PASSWORD, session=session)
        reset_resp = await client.system.async_update(
            12345, {"name": "Updated System Name"}
        )
        assert reset_resp["id"] == 12345
        assert reset_resp["name"] == "Updated System Name"
