"""Define tests for listeners."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

import aiohttp
import pytest
from aresponses import ResponsesMockServer

from aionotion import async_get_client_with_credentials
from tests.common import TEST_EMAIL, TEST_PASSWORD


@pytest.mark.asyncio
async def test_listener_all(
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
            client = await async_get_client_with_credentials(
                TEST_EMAIL, TEST_PASSWORD, session=session
            )
            listeners = await client.listener.async_all()
            assert len(listeners) == 1
            assert listeners[0].id == "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
            assert listeners[0].definition_id == 24
            assert listeners[0].created_at == datetime(
                2019, 6, 17, 3, 29, 45, 722000, tzinfo=timezone.utc
            )
            assert listeners[0].device_type == "sensor"
            assert listeners[0].model_version == "1.0"
            assert listeners[0].sensor_id == "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
            assert listeners[0].status_localized.state == "Idle"
            assert listeners[0].insights.primary.origin is not None
            assert (
                listeners[0].insights.primary.origin.id
                == "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
            )
            assert listeners[0].insights.primary.origin.type == "Sensor"
            assert listeners[0].insights.primary.value == "idle"
            assert listeners[0].insights.primary.data_received_at == datetime(
                2023, 6, 18, 6, 17, 0, 697000, tzinfo=timezone.utc
            )
            assert listeners[0].configuration == {}
            assert listeners[0].pro_monitoring_status == "ineligible"

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_listener_definitions(
    aresponses: ResponsesMockServer,
    authenticated_notion_api_server: ResponsesMockServer,
    listener_definitions_response: dict[str, Any],
) -> None:
    """Test getting listeners for all sensors.

    Args:
        aresponses: An aresponses server.
        authenticated_notion_api_server: A mock authenticated Notion API server
        listener_definitions_response: An API response payload
    """
    async with authenticated_notion_api_server:
        authenticated_notion_api_server.add(
            "api.getnotion.com",
            "/api/listener_definitions",
            "get",
            response=aiohttp.web_response.json_response(
                listener_definitions_response, status=200
            ),
        )

        async with aiohttp.ClientSession() as session:
            client = await async_get_client_with_credentials(
                TEST_EMAIL, TEST_PASSWORD, session=session
            )
            definitions = await client.listener.async_definitions()
            assert len(definitions) == 20
            assert definitions[0].id == 0
            assert definitions[0].name == "battery"
            assert definitions[0].conflict_type == "battery"
            assert definitions[0].priority == 50
            assert definitions[0].hidden is True
            assert definitions[0].conflicting_types == []
            assert definitions[0].resources == {}
            assert definitions[0].compatible_hardware_revisions == [
                3,
                4,
                5,
                6,
                7,
            ]
            assert definitions[0].type == "sensor"

    aresponses.assert_plan_strictly_followed()
