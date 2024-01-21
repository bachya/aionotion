"""Define dynamic test fixtures."""
import json
from collections.abc import Generator
from time import time
from typing import Any, cast

import aiohttp
import pytest
from aresponses import ResponsesMockServer

from tests.common import TEST_USER_UUID, generate_jwt, load_fixture


def _generate_auth_response_success(
    access_token_issued_at: float | None, fixture_filename: str
) -> dict[str, Any]:
    """Generate a successful auth response payload.

    Args:
        access_token_issued_at: A timestamp at which an access token is issued.
        fixture_filename: The name of the fixture file.

    Returns:
        A successful auth response payload.
    """
    if not access_token_issued_at:
        access_token_issued_at = time()
    response: dict[str, Any] = json.loads(load_fixture(fixture_filename))
    response["auth"]["jwt"] = generate_jwt(access_token_issued_at)
    return response


@pytest.fixture(name="auth_failure_response", scope="session")
def auth_failure_response_fixture() -> dict[str, Any]:
    """Return a fixture for a failed auth response payload.

    Returns:
        A fixture for a failed auth response payload.
    """
    return cast(dict[str, Any], json.loads(load_fixture("auth_failure_response.json")))


@pytest.fixture(name="auth_credentials_success_response")
def auth_credentials_success_response_fixture(
    access_token_issued_at: float,
) -> dict[str, Any]:
    """Return a fixture for a successful auth response payload.

    Args:
        access_token_issued_at: A timestamp at which an access token is issued.

    Returns:
        A fixture for a successful auth response payload.
    """
    return _generate_auth_response_success(
        access_token_issued_at, "auth_credentials_success_response.json"
    )


@pytest.fixture(name="auth_legacy_credentials_success_response")
def auth_legacy_credentials_success_response_fixture() -> dict[str, Any]:
    """Return a fixture for a successful auth response payload (legacy)

    Returns:
        A fixture for a successful legacy auth response payload.
    """
    return cast(
        dict[str, Any],
        json.loads(load_fixture("auth_legacy_credentials_success_response.json")),
    )


@pytest.fixture(name="auth_refresh_token_success_response")
def auth_refresh_token_success_response_fixture(
    access_token_issued_at: float,
) -> dict[str, Any]:
    """Return a fixture for a successful auth response payload.

    Args:
        access_token_issued_at: A timestamp at which an access token is issued.

    Returns:
        A fixture for a successful auth response payload.
    """
    return _generate_auth_response_success(
        access_token_issued_at, "auth_refresh_token_success_response.json"
    )


@pytest.fixture(name="access_token_issued_at")
def access_token_issued_at_fixture() -> None:
    """Return a fixture for a timestamp at which an access token is issued.

    We don't use time() as a default because we have some tests where we need this value
    to be different *within* the function (and the fixture's default "function" scope
    will generate a single value for the entire function). By setting this to None,
    downstream fixtures can set a value that works for them.
    """
    return None


@pytest.fixture(name="authenticated_notion_api_server")
def authenticated_notion_api_server_fixture(
    auth_credentials_success_response: dict[str, Any],
    auth_refresh_token_success_response: dict[str, Any],
) -> Generator[ResponsesMockServer, None, None]:
    """Return a fixture that mocks an authenticated Notion API server.

    Args:
        auth_credentials_success_response: An API response payload
        auth_refresh_token_success_response: An API response payload

    Yields:
        A fixture that mocks an authenticated Notion API server.
    """
    server = ResponsesMockServer()
    server.add(
        "api.getnotion.com",
        "/api/auth/login",
        "post",
        response=aiohttp.web_response.json_response(
            auth_credentials_success_response, status=200
        ),
    )
    server.add(
        "api.getnotion.com",
        f"/api/auth/{TEST_USER_UUID}/refresh",
        "post",
        response=aiohttp.web_response.json_response(
            auth_refresh_token_success_response, status=200
        ),
    )
    yield server


@pytest.fixture(name="bad_api_response", scope="session")
def bad_api_response_fixture() -> dict[str, Any]:
    """Return a fixture for a bad API response.

    Returns:
        A fixture for a bad API response.
    """
    return cast(dict[str, Any], json.loads(load_fixture("bad_api_response.json")))


@pytest.fixture(name="bridge_all_response", scope="session")
def bridge_all_response_fixture() -> dict[str, Any]:
    """Return a fixture for a successful GET /api/base_stations response.

    Returns:
        A fixture for a successful GET /api/base_stations response.
    """
    return cast(dict[str, Any], json.loads(load_fixture("bridge_all_response.json")))


@pytest.fixture(name="bridge_get_response", scope="session")
def bridge_get_response_fixture() -> dict[str, Any]:
    """Return a fixture for a successful GET /api/base_stations/<ID> response.

    Returns:
        A fixture for a successful GET /api/base_stations/<ID> response.
    """
    return cast(dict[str, Any], json.loads(load_fixture("bridge_get_response.json")))


@pytest.fixture(name="sensor_all_response", scope="session")
def sensor_all_response_fixture() -> dict[str, Any]:
    """Return a fixture for a successful GET /api/sensors response.

    Returns:
        A fixture for a successful GET /api/sensors response.
    """
    return cast(dict[str, Any], json.loads(load_fixture("sensor_all_response.json")))


@pytest.fixture(name="sensor_get_response", scope="session")
def sensor_get_response_fixture() -> dict[str, Any]:
    """Return a fixture for a successful GET /api/sensors/<ID> response.

    Returns:
        A fixture for a successful GET /api/sensors/<ID> response.
    """
    return cast(dict[str, Any], json.loads(load_fixture("sensor_get_response.json")))


@pytest.fixture(name="sensor_listeners_response", scope="session")
def sensor_listeners_response_fixture() -> dict[str, Any]:
    """Return a fixture for a successful GET /api/sensors/listeners response.

    Returns:
        A fixture for a successful GET /api/sensors/listeners response.
    """
    return cast(
        dict[str, Any], json.loads(load_fixture("sensor_listeners_response.json"))
    )


@pytest.fixture(name="system_all_response", scope="session")
def system_all_response_fixture() -> dict[str, Any]:
    """Return a fixture for a successful GET /api/systems response.

    Returns:
        A fixture for a successful GET /api/systems response.
    """
    return cast(dict[str, Any], json.loads(load_fixture("system_all_response.json")))


@pytest.fixture(name="system_get_response", scope="session")
def system_get_response_fixture() -> dict[str, Any]:
    """Return a fixture for a successful GET /api/systems/<ID> response.

    Returns:
        A fixture for a successful GET /api/systems/<ID> response.
    """
    return cast(dict[str, Any], json.loads(load_fixture("system_get_response.json")))


@pytest.fixture(name="user_preferences_response", scope="session")
def user_preferences_response_fixture() -> dict[str, Any]:
    """Return a fixture for a successful GET /api/users/<ID>/user_preferences response.

    Returns:
        A fixture for a successful GET /api/users/<ID>/user_preferences response.
    """
    return cast(
        dict[str, Any], json.loads(load_fixture("user_preferences_response.json"))
    )
