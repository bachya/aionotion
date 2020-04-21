"""Define tests for sensors."""
import aiohttp
import pytest

from aionotion import async_get_client

from .common import TEST_EMAIL, TEST_PASSWORD, load_fixture


@pytest.mark.asyncio
async def test_sensor_all(aresponses):
    """Test getting all sensors."""
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
        "/api/sensors",
        "get",
        aresponses.Response(text=load_fixture("sensor_all_response.json"), status=200),
    )

    async with aiohttp.ClientSession() as session:
        client = await async_get_client(TEST_EMAIL, TEST_PASSWORD, session=session)
        sensors = await client.sensor.async_all()
        assert len(sensors) == 2


@pytest.mark.asyncio
async def test_sensor_create(aresponses):
    """Test creating a sensor."""
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
        "/api/sensors",
        "post",
        aresponses.Response(
            text=load_fixture("sensor_create_response.json"), status=200
        ),
    )

    async with aiohttp.ClientSession() as session:
        client = await async_get_client(TEST_EMAIL, TEST_PASSWORD, session=session)
        create_resp = await client.sensor.async_create(
            {"name": "New Sensor", "id": 123456}
        )
        assert create_resp["id"] == 123456
        assert create_resp["name"] == "New Sensor"


@pytest.mark.asyncio
async def test_sensor_delete(aresponses):
    """Test deleting a sensor."""
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
        "/api/sensors/123456",
        "delete",
        aresponses.Response(text=None, status=200),
    )

    async with aiohttp.ClientSession() as session:
        client = await async_get_client(TEST_EMAIL, TEST_PASSWORD, session=session)
        await client.sensor.async_delete(123456)


@pytest.mark.asyncio
async def test_sensor_get(aresponses):
    """Test getting a sensor by ID."""
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
        "/api/sensors/123456",
        "get",
        aresponses.Response(text=load_fixture("sensor_get_response.json"), status=200),
    )

    async with aiohttp.ClientSession() as session:
        client = await async_get_client(TEST_EMAIL, TEST_PASSWORD, session=session)
        sensor = await client.sensor.async_get(123456)
        assert sensor["id"] == 123456
        assert sensor["name"] == "Bathroom Sensor"


@pytest.mark.asyncio
async def test_sensor_update(aresponses):
    """Test deleting a sensor."""
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
        "/api/sensors/123456",
        "put",
        aresponses.Response(
            text=load_fixture("sensor_update_response.json"), status=200
        ),
    )

    async with aiohttp.ClientSession() as session:
        client = await async_get_client(TEST_EMAIL, TEST_PASSWORD, session=session)
        reset_resp = await client.sensor.async_update(
            123456, {"name": "Updated Sensor Name"}
        )
        assert reset_resp["id"] == 123456
        assert reset_resp["name"] == "Updated Sensor Name"
