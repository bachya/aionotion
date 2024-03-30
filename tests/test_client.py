"""Define tests for the client."""

# pylint: disable=protected-access
from __future__ import annotations

import asyncio
import logging
from time import time
from typing import Any
from unittest.mock import Mock

import aiohttp
from aresponses import ResponsesMockServer
import pytest

from aionotion import (
    async_get_client_with_credentials,
    async_get_client_with_refresh_token,
)
from aionotion.client import Client
from aionotion.errors import InvalidCredentialsError, RequestError

from .common import TEST_EMAIL, TEST_PASSWORD, TEST_REFRESH_TOKEN, TEST_USER_UUID


@pytest.mark.asyncio()
async def test_api_error(
    aresponses: ResponsesMockServer,
    authenticated_notion_api_server: ResponsesMockServer,
    bad_api_response: dict[str, Any],
) -> None:
    """Test an invalid API call.

    Args:
    ----
        aresponses: An aresponses server
        authenticated_notion_api_server: A mock authenticated Notion API server
        bad_api_response: An API response payload

    """
    async with authenticated_notion_api_server:
        authenticated_notion_api_server.add(
            "api.getnotion.com",
            "/api/bad_endpoint",
            "get",
            response=aiohttp.web_response.json_response(bad_api_response, status=400),
        )

        async with aiohttp.ClientSession() as session:
            with pytest.raises(RequestError):
                client = await async_get_client_with_credentials(
                    TEST_EMAIL, TEST_PASSWORD, session=session
                )
                await client.async_request("get", "/bad_endpoint")

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio()
async def test_auth_credentials_success(
    aresponses: ResponsesMockServer,
    authenticated_notion_api_server: ResponsesMockServer,
) -> None:
    """Test authenticating against the API with credentials.

    Args:
    ----
        aresponses: An aresponses server
        authenticated_notion_api_server: A mock authenticated Notion API server

    """
    async with authenticated_notion_api_server, aiohttp.ClientSession() as session:
        client = await async_get_client_with_credentials(
            TEST_EMAIL, TEST_PASSWORD, session=session
        )
        assert client._access_token is not None

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio()
async def test_auth_failure(
    aresponses: ResponsesMockServer, auth_failure_response: dict[str, Any]
) -> None:
    """Test invalid credentials.

    Args:
    ----
        aresponses: An aresponses server
        auth_failure_response: An API response payload

    """
    aresponses.add(
        "api.getnotion.com",
        "/api/auth/login",
        "post",
        response=aiohttp.web_response.json_response(auth_failure_response, status=401),
    )

    async with aiohttp.ClientSession() as session:
        with pytest.raises(InvalidCredentialsError):
            _ = await async_get_client_with_credentials(
                TEST_EMAIL, TEST_PASSWORD, session=session
            )

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio()
async def test_auth_legacy_credentials_success(
    aresponses: ResponsesMockServer,
    auth_legacy_credentials_success_response: dict[str, Any],
    bridge_all_response: dict[str, Any],
) -> None:
    """Test authenticating against the API with credentials (legacy).

    Args:
    ----
        aresponses: An aresponses server
        auth_legacy_credentials_success_response: An API response payload
        bridge_all_response: An API response payload

    """
    aresponses.add(
        "api.getnotion.com",
        "/api/users/sign_in",
        "post",
        response=aiohttp.web_response.json_response(
            auth_legacy_credentials_success_response, status=200
        ),
    )
    aresponses.add(
        "api.getnotion.com",
        "/api/base_stations",
        "get",
        response=aiohttp.web_response.json_response(bridge_all_response, status=200),
    )

    async with aiohttp.ClientSession() as session:
        client = await async_get_client_with_credentials(
            TEST_EMAIL, TEST_PASSWORD, session=session, use_legacy_auth=True
        )
        assert client._access_token is not None

        bridges = await client.bridge.async_all()
        assert len(bridges) == 1

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio()
async def test_auth_refresh_token_success(
    aresponses: ResponsesMockServer,
    auth_refresh_token_success_response: dict[str, Any],
) -> None:
    """Test authenticating against the API with a refresh token.

    Args:
    ----
        aresponses: An aresponses server
        auth_refresh_token_success_response: An API response payload

    """
    aresponses.add(
        "api.getnotion.com",
        f"/api/auth/{TEST_USER_UUID}/refresh",
        "post",
        response=aiohttp.web_response.json_response(
            auth_refresh_token_success_response, status=200
        ),
    )
    async with aiohttp.ClientSession() as session:
        client = await async_get_client_with_refresh_token(
            TEST_USER_UUID, TEST_REFRESH_TOKEN, session=session
        )
        assert client._access_token is not None

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio()
@pytest.mark.parametrize("refresh_token", [None, "new_refresh_token"])
async def test_auth_refresh_token_success_existing_client(
    aresponses: ResponsesMockServer,
    authenticated_notion_api_server: ResponsesMockServer,
    refresh_token: str | None,
) -> None:
    """Test authenticating against the API with a refresh token with an existing client.

    Args:
    ----
        aresponses: An aresponses server
        authenticated_notion_api_server: A mock authenticated Notion API server
        refresh_token: An optional refresh token

    """
    async with authenticated_notion_api_server, aiohttp.ClientSession() as session:
        client = await async_get_client_with_credentials(
            TEST_EMAIL, TEST_PASSWORD, session=session
        )
        old_access_token = client._access_token
        assert old_access_token is not None
        assert client.refresh_token is not None

        await client.async_authenticate_from_refresh_token(refresh_token=refresh_token)
        new_access_token = client._access_token
        assert new_access_token is not None
        assert old_access_token != new_access_token

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio()
@pytest.mark.parametrize("access_token_issued_at", [time() - 30 * 60])
async def test_expired_access_token(
    aresponses: ResponsesMockServer,
    authenticated_notion_api_server: ResponsesMockServer,
    bridge_all_response: dict[str, Any],
    caplog: Mock,
) -> None:
    """Test handling an expired access token.

    Args:
    ----
        aresponses: An aresponses server
        authenticated_notion_api_server: A mock authenticated Notion API server
        bridge_all_response: An API response payload
        caplog: A mocked logging utility.

    """
    caplog.set_level(logging.DEBUG)

    async with authenticated_notion_api_server, aiohttp.ClientSession() as session:
        authenticated_notion_api_server.add(
            "api.getnotion.com",
            "/api/base_stations",
            "get",
            response=aiohttp.web_response.json_response(
                bridge_all_response, status=200
            ),
        )

        client = await async_get_client_with_credentials(
            TEST_EMAIL, TEST_PASSWORD, session=session
        )
        _ = await client.bridge.async_all()
        assert any(
            m for m in caplog.messages if "Access token expired, refreshing..." in m
        )

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio()
@pytest.mark.parametrize("access_token_issued_at", [time() - 30 * 60])
async def test_expired_access_token_concurrent_calls(
    aresponses: ResponsesMockServer,
    authenticated_notion_api_server: ResponsesMockServer,
    bridge_all_response: dict[str, Any],
    caplog: Mock,
    sensor_all_response: dict[str, Any],
) -> None:
    """Test handling an expired access token with multiple concurrent calls.

    Args:
    ----
        aresponses: An aresponses server
        authenticated_notion_api_server: A mock authenticated Notion API server.
        bridge_all_response: An API response payload.
        caplog: A mocked logging utility.
        sensor_all_response: An API response payload.

    """
    caplog.set_level(logging.DEBUG)

    async with authenticated_notion_api_server, aiohttp.ClientSession() as session:
        authenticated_notion_api_server.add(
            "api.getnotion.com",
            "/api/base_stations",
            "get",
            response=aiohttp.web_response.json_response(
                bridge_all_response, status=200
            ),
        )
        authenticated_notion_api_server.add(
            "api.getnotion.com",
            "/api/sensors",
            "get",
            response=aiohttp.web_response.json_response(
                sensor_all_response, status=200
            ),
        )

        client = await async_get_client_with_credentials(
            TEST_EMAIL, TEST_PASSWORD, session=session
        )

        tasks = [client.bridge.async_all(), client.sensor.async_all()]
        results = await asyncio.gather(*tasks)

        # Assert the we got the results of both calls, even with a refreshed access
        # token in the middle:
        assert len(results) == 2

        assert any(
            m for m in caplog.messages if "Access token expired, refreshing..." in m
        )

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio()
async def test_premature_refresh_token(
    aresponses: ResponsesMockServer,
    authenticated_notion_api_server: ResponsesMockServer,
) -> None:
    """Test attempting to refresh the access token before actually getting one.

    Args:
    ----
        aresponses: An aresponses server
        authenticated_notion_api_server: A mock authenticated Notion API server

    """
    async with authenticated_notion_api_server, aiohttp.ClientSession() as session:
        client = Client(session=session)
        with pytest.raises(InvalidCredentialsError):
            await client.async_authenticate_from_refresh_token()

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio()
async def test_no_explicit_session(
    aresponses: ResponsesMockServer,
    authenticated_notion_api_server: ResponsesMockServer,
) -> None:
    """Test authentication without an explicit ClientSession.

    Args:
    ----
        aresponses: An aresponses server
        authenticated_notion_api_server: A mock authenticated Notion API server

    """
    async with authenticated_notion_api_server:
        client = await async_get_client_with_credentials(TEST_EMAIL, TEST_PASSWORD)
        assert client._access_token is not None

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio()
async def test_refresh_token_callback(
    aresponses: ResponsesMockServer,
    auth_refresh_token_success_response: dict[str, Any],
    authenticated_notion_api_server: ResponsesMockServer,
) -> None:
    """Test that a refresh token callback is called when the access token is refreshed.

    Args:
    ----
        aresponses: An aresponses server
        auth_refresh_token_success_response: An API response payload
        authenticated_notion_api_server: A mock authenticated Notion API server

    """
    async with authenticated_notion_api_server:
        authenticated_notion_api_server.add(
            "api.getnotion.com",
            f"/api/auth/{TEST_USER_UUID}/refresh",
            "post",
            response=aiohttp.web_response.json_response(
                auth_refresh_token_success_response, status=200
            ),
        )

        client = await async_get_client_with_credentials(TEST_EMAIL, TEST_PASSWORD)
        assert client._access_token is not None

        # Define and attach a refresh token callback, then refresh the access token:
        refresh_token_callback = Mock()
        remove_callback = client.add_refresh_token_callback(refresh_token_callback)
        await client.async_authenticate_from_refresh_token()

        # Cancel the callback and refresh the access token again:
        remove_callback()
        await client.async_authenticate_from_refresh_token()

        # Ensure that the callback was called only once:
        refresh_token_callback.assert_called_once_with(client._refresh_token)

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio()
@pytest.mark.parametrize("bridge_get_response", [{}])
async def test_validation_error(
    authenticated_notion_api_server: ResponsesMockServer,
    bridge_get_response: dict[str, Any],
) -> None:
    """Test a response validation error.

    Args:
    ----
        authenticated_notion_api_server: A mock authenticated Notion API server
        bridge_get_response: An API response payload

    """
    async with authenticated_notion_api_server:
        authenticated_notion_api_server.add(
            "api.getnotion.com",
            "/api/base_stations/98765",
            "get",
            response=aiohttp.web_response.json_response(
                bridge_get_response, status=200
            ),
        )

        async with aiohttp.ClientSession() as session:
            client = await async_get_client_with_credentials(
                TEST_EMAIL, TEST_PASSWORD, session=session
            )
            with pytest.raises(RequestError):
                await client.bridge.async_get(98765)
