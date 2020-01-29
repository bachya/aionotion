"""Define tests for the client."""
# pylint: disable=protected-access
import aiohttp
import pytest

from aionotion import async_get_client
from aionotion.errors import InvalidCredentialsError, RequestError

from .common import TEST_EMAIL, TEST_PASSWORD, TEST_TOKEN, load_fixture


@pytest.mark.asyncio
async def test_api_error(aresponses):
    """Test an invalid API call."""
    aresponses.add(
        "api.getnotion.com",
        "/api/users/sign_in",
        "post",
        aresponses.Response(
            text=load_fixture("auth_success_response.json"), status=200
        ),
    )
    aresponses.add(
        "api.getnotion.com",
        "/api/bad_endpoint",
        "get",
        aresponses.Response(text=load_fixture("bad_api_response.json"), status=404),
    )

    async with aiohttp.ClientSession() as websession:
        with pytest.raises(RequestError):
            client = await async_get_client(TEST_EMAIL, TEST_PASSWORD, websession)
            await client._request("get", "bad_endpoint")


@pytest.mark.asyncio
async def test_auth_failure(aresponses):
    """Test invalid credentials."""
    aresponses.add(
        "api.getnotion.com",
        "/api/users/sign_in",
        "post",
        aresponses.Response(
            text=load_fixture("auth_success_response.json"), status=401
        ),
    )

    async with aiohttp.ClientSession() as websession:
        with pytest.raises(InvalidCredentialsError):
            _ = await async_get_client(TEST_EMAIL, TEST_PASSWORD, websession)


@pytest.mark.asyncio
async def test_auth_success(aresponses):
    """Test authenticating against the API and getting a token."""
    aresponses.add(
        "api.getnotion.com",
        "/api/users/sign_in",
        "post",
        aresponses.Response(
            text=load_fixture("auth_success_response.json"), status=200
        ),
    )

    async with aiohttp.ClientSession() as websession:
        client = await async_get_client(TEST_EMAIL, TEST_PASSWORD, websession)
        assert client._token == TEST_TOKEN
