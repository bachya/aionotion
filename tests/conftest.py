"""Define dynamic test fixtures."""
import json
from collections.abc import Generator
from typing import Any, cast

import aiohttp
import pytest
from aresponses import ResponsesMockServer

from tests.common import load_fixture


@pytest.fixture(name="auth_failure_response", scope="session")
def auth_failure_response_fixture() -> dict[str, Any]:
    """Return a fixture for a failed auth response payload."""
    return cast(dict[str, Any], json.loads(load_fixture("auth_failure_response.json")))


@pytest.fixture(name="auth_success_response", scope="session")
def auth_success_response_fixture() -> dict[str, Any]:
    """Return a fixture for a successful auth response payload."""
    return cast(dict[str, Any], json.loads(load_fixture("auth_success_response.json")))


@pytest.fixture(name="authenticated_notion_api_server")
def authenticated_notion_api_server_fixture(
    auth_success_response: dict[str, Any],
) -> Generator[ResponsesMockServer, None, None]:
    """Return a fixture that mocks an authenticated Notion API server.

    Args:
        auth_success_response: An API response payload
    """
    server = ResponsesMockServer()
    server.add(
        "api.getnotion.com",
        "/api/auth/login",
        "post",
        response=aiohttp.web_response.json_response(auth_success_response, status=200),
    )
    yield server


@pytest.fixture(name="bad_api_response", scope="session")
def bad_api_response_fixture() -> dict[str, Any]:
    """Return a fixture for a bad API response."""
    return cast(dict[str, Any], json.loads(load_fixture("bad_api_response.json")))


@pytest.fixture(name="bridge_all_response", scope="session")
def bridge_all_response_fixture() -> dict[str, Any]:
    """Return a fixture for a successful GET /api/base_stations response."""
    return cast(dict[str, Any], json.loads(load_fixture("bridge_all_response.json")))


@pytest.fixture(name="bridge_create_response", scope="session")
def bridge_create_response_fixture() -> dict[str, Any]:
    """Return a fixture for a successful POST /api/base_stations response."""
    return cast(dict[str, Any], json.loads(load_fixture("bridge_create_response.json")))


@pytest.fixture(name="bridge_get_response", scope="session")
def bridge_get_response_fixture() -> dict[str, Any]:
    """Return a fixture for a successful GET /api/base_stations/<ID> response."""
    return cast(dict[str, Any], json.loads(load_fixture("bridge_get_response.json")))


@pytest.fixture(name="bridge_reset_response", scope="session")
def bridge_reset_response_fixture() -> dict[str, Any]:
    """Return a fixture for a successful GET /api/base_stations/<ID>/reset response."""
    return cast(dict[str, Any], json.loads(load_fixture("bridge_reset_response.json")))


@pytest.fixture(name="bridge_update_response", scope="session")
def bridge_update_response_fixture() -> dict[str, Any]:
    """Return a fixture for a successful PUT /api/base_stations/<ID> response."""
    return cast(dict[str, Any], json.loads(load_fixture("bridge_update_response.json")))
