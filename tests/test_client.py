"""Define tests for the client."""
# pylint: disable=protected-access
from __future__ import annotations

from typing import Any

import aiohttp
import pytest
from aresponses import ResponsesMockServer

from aionotion import async_get_client
from aionotion.errors import InvalidCredentialsError, RequestError

from .common import TEST_EMAIL, TEST_PASSWORD, TEST_TOKEN


@pytest.mark.asyncio
async def test_api_error(
    aresponses: ResponsesMockServer,
    authenticated_notion_api_server: ResponsesMockServer,
    bad_api_response: dict[str, Any],
) -> None:
    """Test an invalid API call.

    Args:
        aresponses: An aresponses server.
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
                client = await async_get_client(
                    TEST_EMAIL, TEST_PASSWORD, session=session
                )
                await client._request("get", "bad_endpoint")

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_auth_failure(
    aresponses: ResponsesMockServer, auth_failure_response: dict[str, Any]
) -> None:
    """Test invalid credentials.

    Args:
        aresponses: An aresponses server.
        auth_failure_response: An API response payload
    """
    aresponses.add(
        "api.getnotion.com",
        "/api/users/sign_in",
        "post",
        response=aiohttp.web_response.json_response(auth_failure_response, status=401),
    )

    async with aiohttp.ClientSession() as session:
        with pytest.raises(InvalidCredentialsError):
            _ = await async_get_client(TEST_EMAIL, TEST_PASSWORD, session=session)

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_auth_success(
    aresponses: ResponsesMockServer,
    authenticated_notion_api_server: ResponsesMockServer,
) -> None:
    """Test authenticating against the API and getting a token.

    Args:
        aresponses: An aresponses server.
        authenticated_notion_api_server: A mock authenticated Notion API server
    """
    async with authenticated_notion_api_server, aiohttp.ClientSession() as session:
        client = await async_get_client(TEST_EMAIL, TEST_PASSWORD, session=session)
        assert client._token == TEST_TOKEN

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_no_explicit_session(
    aresponses: ResponsesMockServer,
    authenticated_notion_api_server: ResponsesMockServer,
) -> None:
    """Test authentication without an explicit ClientSession.

    Args:
        aresponses: An aresponses server.
        authenticated_notion_api_server: A mock authenticated Notion API server
    """
    async with authenticated_notion_api_server:
        client = await async_get_client(TEST_EMAIL, TEST_PASSWORD)
        assert client._token == TEST_TOKEN

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
@pytest.mark.parametrize("bridge_get_response", [{}])
async def test_validation_error(
    authenticated_notion_api_server: ResponsesMockServer,
    bridge_get_response: dict[str, Any],
) -> None:
    """Test a response validation error.

    Args:
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
            client = await async_get_client(TEST_EMAIL, TEST_PASSWORD, session=session)
            with pytest.raises(RequestError):
                await client.bridge.async_get(98765)
