"""Define tests for sensors."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

import aiohttp
import pytest
from aresponses import ResponsesMockServer

from aionotion import async_get_client
from aionotion.sensor.models import ListenerKind
from tests.common import TEST_EMAIL, TEST_PASSWORD


@pytest.mark.asyncio
async def test_sensor_all(
    aresponses: ResponsesMockServer,
    authenticated_notion_api_server: ResponsesMockServer,
    sensor_all_response: dict[str, Any],
) -> None:
    """Test getting all sensors.

    Args:
        aresponses: An aresponses server.
        authenticated_notion_api_server: A mock authenticated Notion API server
        sensor_all_response: An API response payload
    """
    async with authenticated_notion_api_server:
        authenticated_notion_api_server.add(
            "api.getnotion.com",
            "/api/sensors",
            "get",
            response=aiohttp.web_response.json_response(
                sensor_all_response, status=200
            ),
        )

        async with aiohttp.ClientSession() as session:
            client = await async_get_client(TEST_EMAIL, TEST_PASSWORD, session=session)
            response = await client.sensor.async_all()
            assert len(response.sensors) == 1
            assert response.sensors[0].id == 123456
            assert response.sensors[0].uuid == "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
            assert response.sensors[0].user.id == 12345
            assert response.sensors[0].user.email == "user@email.com"
            assert response.sensors[0].bridge.id == 67890
            assert response.sensors[0].bridge.hardware_id == "0x0000000000000000"
            assert (
                response.sensors[0].last_bridge_hardware_id
                == "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
            )
            assert response.sensors[0].name == "Sensor 1"
            assert response.sensors[0].location_id == 123456
            assert response.sensors[0].system_id == 12345
            assert response.sensors[0].hardware_id == "0x0000000000000000"
            assert response.sensors[0].hardware_revision == 5
            assert response.sensors[0].firmware_version == "1.1.2"
            assert response.sensors[0].device_key == "0x0000000000000000"
            assert response.sensors[0].encryption_key is True
            assert response.sensors[0].installed_at == datetime(
                2019, 6, 17, 3, 30, 27, 766000, tzinfo=timezone.utc
            )
            assert response.sensors[0].calibrated_at == datetime(
                2024, 1, 19, 0, 38, 15, 372000, tzinfo=timezone.utc
            )
            assert response.sensors[0].last_reported_at == datetime(
                2024, 1, 21, 0, 0, 46, 705000, tzinfo=timezone.utc
            )
            assert response.sensors[0].missing_at is None
            assert response.sensors[0].updated_at == datetime(
                2024, 1, 19, 0, 38, 16, 856000, tzinfo=timezone.utc
            )
            assert response.sensors[0].created_at == datetime(
                2019, 6, 17, 3, 29, 45, 506000, tzinfo=timezone.utc
            )
            assert response.sensors[0].signal_strength == 4
            assert response.sensors[0].firmware.status == "valid"
            assert response.sensors[0].surface_type is None

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_sensor_get(
    aresponses: ResponsesMockServer,
    authenticated_notion_api_server: ResponsesMockServer,
    sensor_get_response: dict[str, Any],
) -> None:
    """Test getting a sensor by ID.

    Args:
        aresponses: An aresponses server.
        authenticated_notion_api_server: A mock authenticated Notion API server
        sensor_get_response: An API response payload
    """
    async with authenticated_notion_api_server:
        authenticated_notion_api_server.add(
            "api.getnotion.com",
            "/api/sensors/123456",
            "get",
            response=aiohttp.web_response.json_response(
                sensor_get_response, status=200
            ),
        )

        async with aiohttp.ClientSession() as session:
            client = await async_get_client(TEST_EMAIL, TEST_PASSWORD, session=session)
            response = await client.sensor.async_get(123456)
            assert response.sensor.id == 123456
            assert response.sensor.uuid == "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
            assert response.sensor.user.id == 12345
            assert response.sensor.user.email == "user@email.com"
            assert response.sensor.bridge.id == 67890
            assert response.sensor.bridge.hardware_id == "0x0000000000000000"
            assert (
                response.sensor.last_bridge_hardware_id
                == "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
            )
            assert response.sensor.name == "Sensor 1"
            assert response.sensor.location_id == 123456
            assert response.sensor.system_id == 12345
            assert response.sensor.hardware_id == "0x0000000000000000"
            assert response.sensor.hardware_revision == 5
            assert response.sensor.firmware_version == "1.1.2"
            assert response.sensor.device_key == "0x0000000000000000"
            assert response.sensor.encryption_key is True
            assert response.sensor.installed_at == datetime(
                2019, 6, 17, 3, 30, 27, 766000, tzinfo=timezone.utc
            )
            assert response.sensor.calibrated_at == datetime(
                2024, 1, 19, 0, 38, 15, 372000, tzinfo=timezone.utc
            )
            assert response.sensor.last_reported_at == datetime(
                2024, 1, 21, 0, 0, 46, 705000, tzinfo=timezone.utc
            )
            assert response.sensor.missing_at is None
            assert response.sensor.updated_at == datetime(
                2024, 1, 19, 0, 38, 16, 856000, tzinfo=timezone.utc
            )
            assert response.sensor.created_at == datetime(
                2019, 6, 17, 3, 29, 45, 506000, tzinfo=timezone.utc
            )
            assert response.sensor.signal_strength == 4
            assert response.sensor.firmware.status == "valid"
            assert response.sensor.surface_type is None

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_sensor_listeners(
    aresponses: ResponsesMockServer,
    authenticated_notion_api_server: ResponsesMockServer,
    sensor_listeners_response: dict[str, Any],
) -> None:
    """Test getting listeners for all sensors.

    Args:
        aresponses: An aresponses server.
        authenticated_notion_api_server: A mock authenticated Notion API server
        sensor_listeners_response: An API response payload
    """
    async with authenticated_notion_api_server:
        authenticated_notion_api_server.add(
            "api.getnotion.com",
            "/api/sensor/listeners",
            "get",
            response=aiohttp.web_response.json_response(
                sensor_listeners_response, status=200
            ),
        )

        async with aiohttp.ClientSession() as session:
            client = await async_get_client(TEST_EMAIL, TEST_PASSWORD, session=session)
            response = await client.sensor.async_listeners()
            assert len(response.listeners) == 1
            assert response.listeners[0].id == "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
            assert response.listeners[0].listener_kind == ListenerKind.UNKNOWN
            assert response.listeners[0].created_at == datetime(
                2019, 6, 17, 3, 29, 45, 722000, tzinfo=timezone.utc
            )
            assert response.listeners[0].device_type == "sensor"
            assert response.listeners[0].model_version == "1.0"
            assert (
                response.listeners[0].sensor_id
                == "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
            )
            assert response.listeners[0].status_localized.state == "Idle"
            assert (
                response.listeners[0].insights.primary.origin.id
                == "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
            )
            assert response.listeners[0].insights.primary.origin.type == "Sensor"
            assert response.listeners[0].insights.primary.value == "idle"
            assert response.listeners[0].insights.primary.data_received_at == datetime(
                2023, 6, 18, 6, 17, 0, 697000, tzinfo=timezone.utc
            )
            assert response.listeners[0].configuration == {}
            assert response.listeners[0].pro_monitoring_status == "ineligible"

    aresponses.assert_plan_strictly_followed()
