"""Define dynamic test fixtures."""
import json
from collections.abc import Generator
from typing import Any, cast

import aiohttp
import pytest
from aresponses import ResponsesMockServer

from .common import load_fixture


@pytest.fixture(name="auth_success_response", scope="session")
def auth_success_response_fixture() -> dict[str, Any]:
    """Return a fixture for a successful auth response payload."""
    return cast(dict[str, Any], json.loads(load_fixture("auth_success_response.json")))


@pytest.fixture(name="authenticated_notion_api_server")
def authenticated_notion_api_server_fixture(
    auth_success_response: dict[str, Any]
) -> Generator[ResponsesMockServer, None, None]:
    """Return a fixture that mocks an authenticated Notion API server.

    Args:
        auth_success_response: An API response payload
    """
    server = ResponsesMockServer()
    server.add(
        "api.getnotion.com",
        "/api/users/sign_in",
        "post",
        response=aiohttp.web_response.json_response(auth_success_response, status=200),
    )
    yield server
