"""Define tests for bridges."""
# pylint: disable=redefined-outer-name, unused-import
import json

import aiohttp
import pytest

from aionotion import async_get_client

from .const import TEST_EMAIL, TEST_PASSWORD
from .fixtures import auth_success_json  # noqa: F401
from .fixtures.bridge import bridge_all_json  # noqa: F401


@pytest.mark.asyncio
async def test_bridge_all(
    aresponses, event_loop, auth_success_json, bridge_all_json  # noqa: F811
):
    """Test getting all bridges."""
    aresponses.add(
        "api.getnotion.com",
        "/api/users/sign_in",
        "post",
        aresponses.Response(text=json.dumps(auth_success_json), status=200),
    )
    aresponses.add(
        "api.getnotion.com",
        "/api/base_stations",
        "get",
        aresponses.Response(text=json.dumps(bridge_all_json), status=200),
    )

    async with aiohttp.ClientSession(loop=event_loop) as websession:
        client = await async_get_client(TEST_EMAIL, TEST_PASSWORD, websession)
        bridges = await client.bridge.async_all()

        assert len(bridges) == 1
