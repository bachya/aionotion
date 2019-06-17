"""Define tests for sensors."""
# pylint: disable=redefined-outer-name, unused-import
import json

import aiohttp
import pytest

from aionotion import async_get_client

from .const import TEST_EMAIL, TEST_PASSWORD
from .fixtures import auth_success_json  # noqa: F401
from .fixtures.sensor import sensor_all_json  # noqa: F401


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
