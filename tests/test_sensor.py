"""Define tests for sensors."""
from __future__ import annotations

import json
from datetime import datetime, timezone

import aiohttp
import pytest
from aresponses import ResponsesMockServer

from aionotion import async_get_client
from aionotion.sensor.models import ListenerKind
from tests.common import TEST_EMAIL, TEST_PASSWORD, load_fixture


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
            assert len(sensors) == 1

            assert sensors[0].id == 123456
            assert sensors[0].uuid == "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
            assert sensors[0].user.id == 12345
            assert sensors[0].user.email == "user@email.com"
            assert sensors[0].bridge.id == 67890
            assert sensors[0].bridge.hardware_id == "0x0000000000000000"
            assert (
                sensors[0].last_bridge_hardware_id
                == "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
            )
            assert sensors[0].name == "Sensor 1"
            assert sensors[0].location_id == 123456
            assert sensors[0].system_id == 12345
            assert sensors[0].hardware_id == "0x0000000000000000"
            assert sensors[0].hardware_revision == 5
            assert sensors[0].firmware_version == "1.1.2"
            assert sensors[0].device_key == "0x0000000000000000"
            assert sensors[0].encryption_key is True
            assert sensors[0].installed_at == datetime(
                2019, 6, 28, 22, 12, 51, 209000, tzinfo=timezone.utc
            )
            assert sensors[0].calibrated_at is None
            assert sensors[0].last_reported_at == datetime(
                2023, 4, 19, 18, 9, 40, 479000, tzinfo=timezone.utc
            )
            assert sensors[0].missing_at is None
            assert sensors[0].updated_at == datetime(
                2023, 3, 28, 13, 33, 33, 801000, tzinfo=timezone.utc
            )
            assert sensors[0].created_at == datetime(
                2019, 6, 28, 22, 12, 20, 256000, tzinfo=timezone.utc
            )
            assert sensors[0].signal_strength == 4
            assert sensors[0].firmware.status == "valid"
            assert sensors[0].surface_type is None

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
            sensor = await client.sensor.async_create(
                {"name": "New Sensor", "id": 123456}
            )
            assert sensor.id == 123456
            assert sensor.uuid == "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
            assert sensor.user.id == 12345
            assert sensor.user.email == "user@email.com"
            assert sensor.bridge.id == 67890
            assert sensor.bridge.hardware_id == "0x0000000000000000"
            assert (
                sensor.last_bridge_hardware_id == "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
            )
            assert sensor.name == "New Sensor"
            assert sensor.location_id == 123456
            assert sensor.system_id == 12345
            assert sensor.hardware_id == "0x0000000000000000"
            assert sensor.hardware_revision == 5
            assert sensor.firmware_version == "1.1.2"
            assert sensor.device_key == "0x0000000000000000"
            assert sensor.encryption_key is True
            assert sensor.installed_at == datetime(
                2019, 6, 28, 22, 12, 51, 209000, tzinfo=timezone.utc
            )
            assert sensor.calibrated_at == datetime(
                2023, 3, 7, 19, 51, 56, 838000, tzinfo=timezone.utc
            )
            assert sensor.last_reported_at == datetime(
                2023, 4, 19, 18, 9, 40, 479000, tzinfo=timezone.utc
            )
            assert sensor.missing_at is None
            assert sensor.updated_at == datetime(
                2023, 3, 28, 13, 33, 33, 801000, tzinfo=timezone.utc
            )
            assert sensor.created_at == datetime(
                2019, 6, 28, 22, 12, 20, 256000, tzinfo=timezone.utc
            )
            assert sensor.signal_strength == 4
            assert sensor.firmware.status == "valid"
            assert sensor.surface_type is None

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
            assert sensor.id == 123456
            assert sensor.uuid == "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
            assert sensor.user.id == 12345
            assert sensor.user.email == "user@email.com"
            assert sensor.bridge.id == 67890
            assert sensor.bridge.hardware_id == "0x0000000000000000"
            assert (
                sensor.last_bridge_hardware_id == "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
            )
            assert sensor.name == "Sensor 1"
            assert sensor.location_id == 123456
            assert sensor.system_id == 12345
            assert sensor.hardware_id == "0x0000000000000000"
            assert sensor.hardware_revision == 5
            assert sensor.firmware_version == "1.1.2"
            assert sensor.device_key == "0x0000000000000000"
            assert sensor.encryption_key is True
            assert sensor.installed_at == datetime(
                2019, 6, 28, 22, 12, 51, 209000, tzinfo=timezone.utc
            )
            assert sensor.calibrated_at == datetime(
                2023, 3, 7, 19, 51, 56, 838000, tzinfo=timezone.utc
            )
            assert sensor.last_reported_at == datetime(
                2023, 4, 19, 18, 9, 40, 479000, tzinfo=timezone.utc
            )
            assert sensor.missing_at is None
            assert sensor.updated_at == datetime(
                2023, 3, 28, 13, 33, 33, 801000, tzinfo=timezone.utc
            )
            assert sensor.created_at == datetime(
                2019, 6, 28, 22, 12, 20, 256000, tzinfo=timezone.utc
            )
            assert sensor.signal_strength == 4
            assert sensor.firmware.status == "valid"
            assert sensor.surface_type is None

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
            listeners = await client.sensor.async_listeners()
            assert len(listeners) == 2

            assert listeners[0].id == "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
            assert listeners[0].listener_kind == ListenerKind.UNKNOWN
            assert listeners[0].created_at == datetime(
                2019, 6, 28, 22, 12, 20, 497000, tzinfo=timezone.utc
            )
            assert listeners[0].device_type == "sensor"
            assert listeners[0].model_version == "1.0"
            assert listeners[0].sensor_id == "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
            assert listeners[0].status is None
            assert listeners[0].status_localized is None
            assert listeners[0].insights.primary.origin is None
            assert listeners[0].insights.primary.value is None
            assert listeners[0].insights.primary.data_received_at is None
            assert listeners[0].configuration == {}
            assert listeners[0].pro_monitoring_status == "ineligible"

            assert listeners[1].id == "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
            assert listeners[1].listener_kind == ListenerKind.LEAK_STATUS
            assert listeners[1].created_at == datetime(
                2019, 6, 28, 22, 12, 49, 651000, tzinfo=timezone.utc
            )
            assert listeners[1].device_type == "sensor"
            assert listeners[1].model_version == "2.1"
            assert listeners[1].sensor_id == "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
            assert listeners[1].status is not None
            assert listeners[1].status.trigger_value == "no_leak"
            assert listeners[1].status.data_received_at == datetime(
                2022, 3, 20, 8, 0, 29, 763000, tzinfo=timezone.utc
            )
            assert listeners[1].status_localized is not None
            assert listeners[1].status_localized.state == "No Leak"
            assert listeners[1].status_localized.description == "Mar 20 at 2:00am"
            assert listeners[1].insights.primary.origin
            assert listeners[1].insights.primary.origin.type == "Sensor"
            assert (
                listeners[1].insights.primary.origin.id
                == "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
            )
            assert listeners[1].insights.primary.value == "no_leak"
            assert listeners[1].insights.primary.data_received_at == datetime(
                2022, 3, 20, 8, 0, 29, 763000, tzinfo=timezone.utc
            )
            assert listeners[1].configuration == {}
            assert listeners[1].pro_monitoring_status == "eligible"

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
            listeners = await client.sensor.async_listeners_for_sensor(
                "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
            )
            assert len(listeners) == 2

            assert listeners[0].id == "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
            assert listeners[0].listener_kind == ListenerKind.UNKNOWN
            assert listeners[0].created_at == datetime(
                2019, 6, 28, 22, 12, 20, 497000, tzinfo=timezone.utc
            )
            assert listeners[0].device_type == "sensor"
            assert listeners[0].model_version == "1.0"
            assert listeners[0].sensor_id == "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
            assert listeners[0].status is not None
            assert listeners[0].status.trigger_value == ""
            assert listeners[0].status.data_received_at == datetime(
                2019, 6, 28, 22, 12, 20, 498000, tzinfo=timezone.utc
            )
            assert listeners[0].status_localized is not None
            assert listeners[0].status_localized.state == "Unknown"
            assert listeners[0].status_localized.description == "Jun 28 at 4:12pm"
            assert listeners[0].insights.primary.origin is None
            assert listeners[0].insights.primary.value is None
            assert listeners[0].insights.primary.data_received_at is None
            assert listeners[0].configuration == {}
            assert listeners[0].pro_monitoring_status == "ineligible"

            assert listeners[1].id == "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
            assert listeners[1].listener_kind == ListenerKind.LEAK_STATUS
            assert listeners[1].created_at == datetime(
                2019, 6, 28, 22, 12, 49, 651000, tzinfo=timezone.utc
            )
            assert listeners[1].device_type == "sensor"
            assert listeners[1].model_version == "2.1"
            assert listeners[1].sensor_id == "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
            assert listeners[1].status is not None
            assert listeners[1].status.trigger_value == "no_leak"
            assert listeners[1].status.data_received_at == datetime(
                2022, 3, 20, 8, 0, 29, 763000, tzinfo=timezone.utc
            )
            assert listeners[1].status_localized is not None
            assert listeners[1].status_localized.state == "No Leak"
            assert listeners[1].status_localized.description == "Mar 20 at 2:00am"
            assert listeners[1].insights.primary.origin
            assert listeners[1].insights.primary.origin.type == "Sensor"
            assert (
                listeners[1].insights.primary.origin.id
                == "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
            )
            assert listeners[1].insights.primary.value == "no_leak"
            assert listeners[1].insights.primary.data_received_at == datetime(
                2022, 3, 20, 8, 0, 29, 763000, tzinfo=timezone.utc
            )
            assert listeners[1].configuration == {}
            assert listeners[1].pro_monitoring_status == "eligible"

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
            sensor = await client.sensor.async_update(
                123456, {"name": "Updated Sensor Name"}
            )
            assert sensor.id == 123456
            assert sensor.uuid == "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
            assert sensor.user.id == 12345
            assert sensor.user.email == "user@email.com"
            assert sensor.bridge.id == 67890
            assert sensor.bridge.hardware_id == "0x0000000000000000"
            assert (
                sensor.last_bridge_hardware_id == "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
            )
            assert sensor.name == "Updated Sensor Name"
            assert sensor.location_id == 123456
            assert sensor.system_id == 12345
            assert sensor.hardware_id == "0x0000000000000000"
            assert sensor.hardware_revision == 5
            assert sensor.firmware_version == "1.1.2"
            assert sensor.device_key == "0x0000000000000000"
            assert sensor.encryption_key is True
            assert sensor.installed_at == datetime(
                2019, 6, 28, 22, 12, 51, 209000, tzinfo=timezone.utc
            )
            assert sensor.calibrated_at == datetime(
                2023, 3, 7, 19, 51, 56, 838000, tzinfo=timezone.utc
            )
            assert sensor.last_reported_at == datetime(
                2023, 4, 19, 18, 9, 40, 479000, tzinfo=timezone.utc
            )
            assert sensor.missing_at is None
            assert sensor.updated_at == datetime(
                2023, 3, 28, 13, 33, 33, 801000, tzinfo=timezone.utc
            )
            assert sensor.created_at == datetime(
                2019, 6, 28, 22, 12, 20, 256000, tzinfo=timezone.utc
            )
            assert sensor.signal_strength == 4
            assert sensor.firmware.status == "valid"
            assert sensor.surface_type is None

    aresponses.assert_plan_strictly_followed()
