"""Define tests for the client."""
# pylint: disable=protected-access,redefined-outer-name,unused-import
import json

import aiohttp
import pytest

from aionotion import async_get_client
from aionotion.errors import RequestError

from .const import TEST_EMAIL, TEST_PASSWORD, TEST_TOKEN
from .fixtures import auth_success_json, bad_api_json  # noqa: F401


@pytest.mark.asyncio
async def test_api_error(
    aresponses, auth_success_json, bad_api_json, event_loop  # noqa: F811
):
    """Test an invalid API call."""
    aresponses.add(
        "api.getnotion.com",
        "/api/users/sign_in",
        "post",
        aresponses.Response(text=json.dumps(auth_success_json), status=200),
    )
    aresponses.add(
        "api.getnotion.com",
        "/api/bad_endpoint",
        "get",
        aresponses.Response(text=json.dumps(bad_api_json), status=404),
    )

    async with aiohttp.ClientSession(loop=event_loop) as websession:
        with pytest.raises(RequestError):
            client = await async_get_client(TEST_EMAIL, TEST_PASSWORD, websession)
            await client._request("get", "bad_endpoint")


@pytest.mark.asyncio
async def test_auth_success(aresponses, auth_success_json, event_loop):  # noqa: F811
    """Test authenticating against the API and getting a token."""
    aresponses.add(
        "api.getnotion.com",
        "/api/users/sign_in",
        "post",
        aresponses.Response(text=json.dumps(auth_success_json), status=200),
    )

    async with aiohttp.ClientSession(loop=event_loop) as websession:
        client = await async_get_client(TEST_EMAIL, TEST_PASSWORD, websession)

        assert client._token == TEST_TOKEN  # pylint: disable=protected-access
