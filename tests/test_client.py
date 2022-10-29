"""Define tests for the client."""
# pylint: disable=protected-access
import json

import aiohttp
import pytest
from aresponses import ResponsesMockServer

from aionotion import async_get_client
from aionotion.errors import InvalidCredentialsError, RequestError

from .common import TEST_EMAIL, TEST_PASSWORD, TEST_TOKEN, load_fixture


@pytest.mark.asyncio
async def test_api_error(
    aresponses: ResponsesMockServer,
    authenticated_notion_api_server: ResponsesMockServer,
) -> None:
    """Test an invalid API call.

    Args:
        aresponses: An aresponses server.
        authenticated_notion_api_server: A mock authenticated Notion API server
    """
    async with authenticated_notion_api_server:
        authenticated_notion_api_server.add(
            "api.getnotion.com",
            "/api/bad_endpoint",
            "get",
            response=aiohttp.web_response.json_response(
                json.loads(load_fixture("bad_api_response.json")), status=404
            ),
        )

        async with aiohttp.ClientSession() as session:
            with pytest.raises(RequestError):
                client = await async_get_client(
                    TEST_EMAIL, TEST_PASSWORD, session=session
                )
                await client._request("get", "bad_endpoint")

    aresponses.assert_plan_strictly_followed()


@pytest.mark.asyncio
async def test_auth_failure(aresponses: ResponsesMockServer) -> None:
    """Test invalid credentials.

    Args:
        aresponses: An aresponses server.
    """
    aresponses.add(
        "api.getnotion.com",
        "/api/users/sign_in",
        "post",
        response=aiohttp.web_response.json_response(
            json.loads(load_fixture("auth_failure_response.json")), status=401
        ),
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
