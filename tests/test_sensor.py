"""Define tests for sensors."""
# pylint: disable=redefined-outer-name, unused-import
import json

import aiohttp
import pytest

from aionotion import async_get_client

from .const import TEST_EMAIL, TEST_PASSWORD
from .fixtures import auth_success_json  # noqa: F401
from .fixtures.sensor import (  # noqa: F401
    sensor_all_json,
    sensor_create_json,
    sensor_get_json,
    sensor_update_json,
)


@pytest.mark.asyncio
async def test_sensor_all(
    aresponses, event_loop, auth_success_json, sensor_all_json  # noqa: F811
):
    """Test getting all sensors."""
    aresponses.add(
        "api.getnotion.com",
        "/api/users/sign_in",
        "post",
        aresponses.Response(text=json.dumps(auth_success_json), status=200),
    )
    aresponses.add(
        "api.getnotion.com",
        "/api/sensors",
        "get",
        aresponses.Response(text=json.dumps(sensor_all_json), status=200),
    )

    async with aiohttp.ClientSession(loop=event_loop) as websession:
        client = await async_get_client(TEST_EMAIL, TEST_PASSWORD, websession)
        sensors = await client.sensor.async_all()

        assert len(sensors) == 2


@pytest.mark.asyncio
async def test_sensor_create(
    aresponses, event_loop, auth_success_json, sensor_create_json  # noqa: F811
):
    """Test creating a sensor."""
    aresponses.add(
        "api.getnotion.com",
        "/api/users/sign_in",
        "post",
        aresponses.Response(text=json.dumps(auth_success_json), status=200),
    )
    aresponses.add(
        "api.getnotion.com",
        "/api/sensors",
        "post",
        aresponses.Response(text=json.dumps(sensor_create_json), status=200),
    )

    async with aiohttp.ClientSession(loop=event_loop) as websession:
        client = await async_get_client(TEST_EMAIL, TEST_PASSWORD, websession)
        create_resp = await client.sensor.async_create(
            {"name": "New Sensor", "id": 123456}
        )

        assert create_resp["id"] == 123456
        assert create_resp["name"] == "New Sensor"


@pytest.mark.asyncio
async def test_sensor_delete(aresponses, event_loop, auth_success_json):  # noqa: F811
    """Test deleting a sensor."""
    aresponses.add(
        "api.getnotion.com",
        "/api/users/sign_in",
        "post",
        aresponses.Response(text=json.dumps(auth_success_json), status=200),
    )
    aresponses.add(
        "api.getnotion.com",
        "/api/sensors/123456",
        "delete",
        aresponses.Response(text=None, status=200),
    )

    async with aiohttp.ClientSession(loop=event_loop) as websession:
        client = await async_get_client(TEST_EMAIL, TEST_PASSWORD, websession)
        await client.sensor.async_delete(123456)


@pytest.mark.asyncio
async def test_sensor_get(
    aresponses, event_loop, auth_success_json, sensor_get_json  # noqa: F811
):
    """Test getting a sensor by ID."""
    aresponses.add(
        "api.getnotion.com",
        "/api/users/sign_in",
        "post",
        aresponses.Response(text=json.dumps(auth_success_json), status=200),
    )
    aresponses.add(
        "api.getnotion.com",
        "/api/sensors/123456",
        "get",
        aresponses.Response(text=json.dumps(sensor_get_json), status=200),
    )

    async with aiohttp.ClientSession(loop=event_loop) as websession:
        client = await async_get_client(TEST_EMAIL, TEST_PASSWORD, websession)
        sensor = await client.sensor.async_get(123456)

        assert sensor["id"] == 123456
        assert sensor["name"] == "Bathroom Sensor"


@pytest.mark.asyncio
async def test_sensor_update(
    aresponses, event_loop, auth_success_json, sensor_update_json  # noqa: F811
):
    """Test deleting a sensor."""
    aresponses.add(
        "api.getnotion.com",
        "/api/users/sign_in",
        "post",
        aresponses.Response(text=json.dumps(auth_success_json), status=200),
    )
    aresponses.add(
        "api.getnotion.com",
        "/api/sensors/123456",
        "put",
        aresponses.Response(text=json.dumps(sensor_update_json), status=200),
    )

    async with aiohttp.ClientSession(loop=event_loop) as websession:
        client = await async_get_client(TEST_EMAIL, TEST_PASSWORD, websession)
        reset_resp = await client.sensor.async_update(
            123456, {"name": "Updated Sensor Name"}
        )

        assert reset_resp["id"] == 123456
        assert reset_resp["name"] == "Updated Sensor Name"
