"""Define tests for the REST API."""
import json

import aiohttp
import pytest

from aionotion import async_get_client
from aionotion.errors import RequestError

from .const import TEST_EMAIL, TEST_PASSWORD, TEST_TOKEN
from .fixtures.api import (
    sign_in_json, systems_json, base_stations_json, sensors_json, tasks_json)


@pytest.mark.asyncio
async def test_api_error(aresponses, event_loop):
    aresponses.add(
        "api.getnotion.com",
        "/api/users/sign_in",
        "post",
        aresponses.Response(text="", status=500),
    )

    async with aiohttp.ClientSession(loop=event_loop) as websession:
        with pytest.raises(RequestError):
            await async_get_client(TEST_EMAIL, TEST_PASSWORD, websession)


@pytest.mark.asyncio
async def test_sign_in(aresponses, event_loop, sign_in_json):
    aresponses.add(
        "api.getnotion.com",
        "/api/users/sign_in",
        "post",
        aresponses.Response(text=json.dumps(sign_in_json), status=200),
    )

    async with aiohttp.ClientSession(loop=event_loop) as websession:
        client = await async_get_client(TEST_EMAIL, TEST_PASSWORD, websession)

        assert client._token == TEST_TOKEN


@pytest.mark.asyncio
async def test_get_systems(aresponses, event_loop, sign_in_json, systems_json):
    aresponses.add(
        "api.getnotion.com",
        "/api/users/sign_in",
        "post",
        aresponses.Response(text=json.dumps(sign_in_json), status=200),
    )
    aresponses.add(
        "api.getnotion.com",
        "/api/systems",
        "get",
        aresponses.Response(text=json.dumps(systems_json), status=200),
    )

    async with aiohttp.ClientSession(loop=event_loop) as websession:
        client = await async_get_client(TEST_EMAIL, TEST_PASSWORD, websession)
        systems = await client.async_get_systems()

        assert len(systems) == 1


@pytest.mark.asyncio
async def test_get_base_stations(
        aresponses, event_loop, sign_in_json, base_stations_json):
    aresponses.add(
        "api.getnotion.com",
        "/api/users/sign_in",
        "post",
        aresponses.Response(text=json.dumps(sign_in_json), status=200),
    )
    aresponses.add(
        "api.getnotion.com",
        "/api/base_stations",
        "get",
        aresponses.Response(text=json.dumps(base_stations_json), status=200),
    )

    async with aiohttp.ClientSession(loop=event_loop) as websession:
        client = await async_get_client(TEST_EMAIL, TEST_PASSWORD, websession)
        base_stations = await client.async_get_base_stations()

        assert len(base_stations) == 1


@pytest.mark.asyncio
async def test_get_sensors(aresponses, event_loop, sign_in_json, sensors_json):
    aresponses.add(
        "api.getnotion.com",
        "/api/users/sign_in",
        "post",
        aresponses.Response(text=json.dumps(sign_in_json), status=200),
    )
    aresponses.add(
        "api.getnotion.com",
        "/api/sensors",
        "get",
        aresponses.Response(text=json.dumps(sensors_json), status=200),
    )

    async with aiohttp.ClientSession(loop=event_loop) as websession:
        client = await async_get_client(TEST_EMAIL, TEST_PASSWORD, websession)
        sensors = await client.async_get_sensors()

        assert len(sensors) == 2


@pytest.mark.asyncio
async def test_get_tasks(aresponses, event_loop, sign_in_json, tasks_json):
    aresponses.add(
        "api.getnotion.com",
        "/api/users/sign_in",
        "post",
        aresponses.Response(text=json.dumps(sign_in_json), status=200),
    )
    aresponses.add(
        "api.getnotion.com",
        "/api/tasks",
        "get",
        aresponses.Response(text=json.dumps(tasks_json), status=200),
    )

    async with aiohttp.ClientSession(loop=event_loop) as websession:
        client = await async_get_client(TEST_EMAIL, TEST_PASSWORD, websession)
        tasks = await client.async_get_tasks()

        assert len(tasks) == 7
