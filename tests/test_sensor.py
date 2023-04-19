"""Define tests for sensors."""
import json

import aiohttp
import pytest
from aresponses import ResponsesMockServer

from aionotion import async_get_client

from .common import TEST_EMAIL, TEST_PASSWORD, load_fixture


@pytest.mark.asyncio
async def test_sensor_all(
    aresponses: ResponsesMockServer,
    authenticated_notion_api_server: ResponsesMockServer,
) -> None:
    """Test getting all sensors.

    Args:
        aresponses: An aresponses server.
        authenticated_notion_api_server: A mock authenticated Notion API server
    """
    async with authenticated_notion_api_server:
        authenticated_notion_api_server.add(
            "api.getnotion.com",
            "/api/sensors",
            "get",
            response=aiohttp.web_response.json_response(
                json.loads(load_fixture("sensor_all_response.json")), status=200
            ),
        )

        async with aiohttp.ClientSession() as session:
            client = await async_get_client(TEST_EMAIL, TEST_PASSWORD, session=session)
            sensors = await client.sensor.async_all()
            assert len(sensors) == 2

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_sensor_create(
    aresponses: ResponsesMockServer,
    authenticated_notion_api_server: ResponsesMockServer,
) -> None:
    """Test creating a sensor.

    Args:
        aresponses: An aresponses server.
        authenticated_notion_api_server: A mock authenticated Notion API server
    """
    async with authenticated_notion_api_server:
        authenticated_notion_api_server.add(
            "api.getnotion.com",
            "/api/sensors",
            "post",
            response=aiohttp.web_response.json_response(
                json.loads(load_fixture("sensor_create_response.json")), status=200
            ),
        )

        async with aiohttp.ClientSession() as session:
            client = await async_get_client(TEST_EMAIL, TEST_PASSWORD, session=session)
            create_resp = await client.sensor.async_create(
                {"name": "New Sensor", "id": 123456}
            )
            assert create_resp["id"] == 123456
            assert create_resp["name"] == "New Sensor"

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_sensor_delete(
    aresponses: ResponsesMockServer,
    authenticated_notion_api_server: ResponsesMockServer,
) -> None:
    """Test deleting a sensor.

    Args:
        aresponses: An aresponses server.
        authenticated_notion_api_server: A mock authenticated Notion API server
    """
    async with authenticated_notion_api_server:
        authenticated_notion_api_server.add(
            "api.getnotion.com",
            "/api/sensors/123456",
            "delete",
            aresponses.Response(
                text=None,
                status=200,
                headers={"Content-Type": "application/json; charset=utf-8"},
            ),
        )

        async with aiohttp.ClientSession() as session:
            client = await async_get_client(TEST_EMAIL, TEST_PASSWORD, session=session)
            await client.sensor.async_delete(123456)

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_sensor_get(
    aresponses: ResponsesMockServer,
    authenticated_notion_api_server: ResponsesMockServer,
) -> None:
    """Test getting a sensor by ID.

    Args:
        aresponses: An aresponses server.
        authenticated_notion_api_server: A mock authenticated Notion API server
    """
    async with authenticated_notion_api_server:
        authenticated_notion_api_server.add(
            "api.getnotion.com",
            "/api/sensors/123456",
            "get",
            response=aiohttp.web_response.json_response(
                json.loads(load_fixture("sensor_get_response.json")), status=200
            ),
        )

        async with aiohttp.ClientSession() as session:
            client = await async_get_client(TEST_EMAIL, TEST_PASSWORD, session=session)
            sensor = await client.sensor.async_get(123456)
            assert sensor["id"] == 123456
            assert sensor["name"] == "Bathroom Sensor"

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_sensor_listeners(
    aresponses: ResponsesMockServer,
    authenticated_notion_api_server: ResponsesMockServer,
) -> None:
    """Test getting listeners for all sensors.

    Args:
        aresponses: An aresponses server.
        authenticated_notion_api_server: A mock authenticated Notion API server
    """
    async with authenticated_notion_api_server:
        authenticated_notion_api_server.add(
            "api.getnotion.com",
            "/api/sensor/listeners",
            "get",
            response=aiohttp.web_response.json_response(
                json.loads(load_fixture("sensor_listeners.json")), status=200
            ),
        )

        async with aiohttp.ClientSession() as session:
            client = await async_get_client(TEST_EMAIL, TEST_PASSWORD, session=session)
            sensors = await client.sensor.async_listeners()
            assert len(sensors) == 2

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_sensor_listeners_for_sensor(
    aresponses: ResponsesMockServer,
    authenticated_notion_api_server: ResponsesMockServer,
) -> None:
    """Test getting listeners for a specific sensor.

    Args:
        aresponses: An aresponses server.
        authenticated_notion_api_server: A mock authenticated Notion API server
    """
    async with authenticated_notion_api_server:
        authenticated_notion_api_server.add(
            "api.getnotion.com",
            "/api/sensors/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx/listeners",
            "get",
            response=aiohttp.web_response.json_response(
                json.loads(load_fixture("sensor_listeners_for_sensor.json")), status=200
            ),
        )

        async with aiohttp.ClientSession() as session:
            client = await async_get_client(TEST_EMAIL, TEST_PASSWORD, session=session)
            sensors = await client.sensor.async_listeners_for_sensor(
                "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
            )
            assert len(sensors) == 2

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_sensor_update(
    aresponses: ResponsesMockServer,
    authenticated_notion_api_server: ResponsesMockServer,
) -> None:
    """Test deleting a sensor.

    Args:
        aresponses: An aresponses server.
        authenticated_notion_api_server: A mock authenticated Notion API server
    """
    async with authenticated_notion_api_server:
        authenticated_notion_api_server.add(
            "api.getnotion.com",
            "/api/sensors/123456",
            "put",
            response=aiohttp.web_response.json_response(
                json.loads(load_fixture("sensor_update_response.json")), status=200
            ),
        )

        async with aiohttp.ClientSession() as session:
            client = await async_get_client(TEST_EMAIL, TEST_PASSWORD, session=session)
            reset_resp = await client.sensor.async_update(
                123456, {"name": "Updated Sensor Name"}
            )
            assert reset_resp["id"] == 123456
            assert reset_resp["name"] == "Updated Sensor Name"

    aresponses.assert_plan_strictly_followed()
