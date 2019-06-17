"""Define tests for the client."""
# pylint: disable=redefined-outer-name, unused-import
import json

import aiohttp
import pytest

from aionotion import async_get_client
from aionotion.errors import RequestError

from .const import TEST_EMAIL, TEST_PASSWORD, TEST_TOKEN
from .fixtures import auth_success_json  # noqa: F401


@pytest.mark.asyncio
async def test_api_error(aresponses, event_loop):
    """Test an invalid API call."""
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
async def test_auth_success(aresponses, event_loop, auth_success_json):  # noqa: F811
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
