"""Define a base client for interacting with Notion."""

from __future__ import annotations

import asyncio
from collections.abc import Callable
from datetime import datetime
from typing import Any, TypeVar, cast
from uuid import uuid4

from aiohttp import ClientSession, ClientTimeout
from aiohttp.client_exceptions import ClientError
from mashumaro import DataClassDictMixin
from mashumaro.exceptions import (
    MissingField,
    SuitableVariantNotFoundError,
    UnserializableDataError,
)

from aionotion.bridge import Bridge
from aionotion.const import LOGGER
from aionotion.errors import InvalidCredentialsError, RequestError
from aionotion.listener import Listener
from aionotion.sensor import Sensor
from aionotion.system import System
from aionotion.user import User
from aionotion.user.models import (
    AuthenticateViaCredentialsLegacyResponse,
    AuthenticateViaCredentialsResponse,
    AuthenticateViaRefreshTokenResponse,
)
from aionotion.util.auth import decode_jwt
from aionotion.util.dt import utc_from_timestamp, utcnow

API_BASE = "https://api.getnotion.com/api"

DEFAULT_TIMEOUT = 10

NotionBaseModelT = TypeVar("NotionBaseModelT", bound=DataClassDictMixin)
RefreshTokenCallbackT = Callable[[str], None]


def get_token_header_value(access_token: str, refresh_token: str | None) -> str:
    """Return the value for the Authorization header.

    The old API uses a different format for the Authorization header than the new API.
    We detect whether we're using the new API by checking whether a refresh token is
    present.

    Args:
        access_token: An access token.
        refresh_token: A refresh token (if it exists).

    Returns:
        The value for the Authorization header.
    """
    if refresh_token:
        return f"Bearer {access_token}"
    return f"Token token={access_token}"


class Client:
    """Define the API object."""

    def __init__(
        self, *, session: ClientSession | None = None, session_name: str | None = None
    ) -> None:
        """Initialize.

        Args:
            session: An optional aiohttp ClientSession.
            session_name: An optional session name to use for authentication.
        """
        self._access_token: str | None = None
        self._access_token_expires_at: datetime | None = None
        self._refresh_event = asyncio.Event()
        self._refresh_lock = asyncio.Lock()
        self._refresh_token: str | None = None
        self._refresh_token_callbacks: list[RefreshTokenCallbackT] = []
        self._refreshing = False
        self._session = session
        self._session_name = session_name or uuid4().hex
        self.user_uuid: str = ""

        self.bridge = Bridge(self)
        self.listener = Listener(self)
        self.sensor = Sensor(self)
        self.system = System(self)
        self.user = User(self)

    @property
    def refresh_token(self) -> str | None:
        """Return the refresh token."""
        return self._refresh_token

    def _save_tokens_from_auth_response(
        self,
        auth_response: AuthenticateViaCredentialsResponse
        | AuthenticateViaRefreshTokenResponse,
    ) -> None:
        """Save the authentication and refresh tokens from an auth response.

        Args:
            auth: An API response containing auth info.
        """
        self._access_token = auth_response.auth.jwt
        self._refresh_token = auth_response.auth.refresh_token

        # Determine the expiration time of the access token:
        decoded_jwt = decode_jwt(self._access_token)
        self._access_token_expires_at = utc_from_timestamp(decoded_jwt["exp"])

        # Call all refresh token callbacks:
        for callback in self._refresh_token_callbacks:
            callback(self._refresh_token)

    def add_refresh_token_callback(
        self, callback: RefreshTokenCallbackT
    ) -> Callable[[], None]:
        """Add a callback to be called when the refresh token is updated."""
        self._refresh_token_callbacks.append(callback)

        def remove_callback() -> None:
            """Remove the callback from the list of callbacks."""
            self._refresh_token_callbacks.remove(callback)

        return remove_callback

    async def async_authenticate_from_credentials(
        self, email: str, password: str
    ) -> None:
        """Authenticate via username and password.

        Args:
            email: The email address of a Notion account.
            password: The account password.
        """
        auth_response: AuthenticateViaCredentialsResponse = (
            await self.async_request_and_validate(
                "post",
                "/auth/login",
                AuthenticateViaCredentialsResponse,
                headers={"Accept-Version": "2"},
                json={
                    "auth": {
                        "email": email,
                        "password": password,
                        "session_name": self._session_name,
                    }
                },
            )
        )

        self.user_uuid = auth_response.user.uuid
        self._save_tokens_from_auth_response(auth_response)

    async def async_authenticate_from_refresh_token(
        self, *, refresh_token: str | None = None
    ) -> None:
        """Authenticate via a refresh token.

        Args:
            refresh_token: The refresh token to use. If not provided, the refresh token
                that was used to authenticate the user initially will be used.

        Raises:
            InvalidCredentialsError: If no refresh token is provided and the user has
                not been authenticated yet.
        """
        if refresh_token is None and self._refresh_token is None:
            raise InvalidCredentialsError("No valid refresh token provided")

        self._refreshing = True

        async with self._refresh_lock:
            # If a refresh token is explicitly provided, use it:
            if refresh_token:
                self._refresh_token = refresh_token

            assert self._refresh_token is not None

            self._refresh_event.clear()

            try:
                auth_response: AuthenticateViaRefreshTokenResponse = (
                    await self.async_request_and_validate(
                        "post",
                        f"/auth/{self.user_uuid}/refresh",
                        AuthenticateViaRefreshTokenResponse,
                        refresh_request=True,
                        headers={"Accept-Version": "2"},
                        json={
                            "auth": {
                                "refresh_token": self._refresh_token,
                            }
                        },
                    )
                )
                self._save_tokens_from_auth_response(auth_response)
            finally:
                self._refreshing = False
                self._refresh_event.set()

    async def async_legacy_authenticate_from_credentials(
        self, email: str, password: str
    ) -> None:
        """Authenticate via username and password (via a legacy endpoint).

        This is kept in place for compatibility, but should be considered deprecated.

        Args:
            email: The email address of a Notion account.
            password: The account password.
        """
        LOGGER.warning(
            "Using legacy authentication endpoint; this is deprecated and will be "
            "removed in a future release"
        )
        auth_response: AuthenticateViaCredentialsLegacyResponse = (
            await self.async_request_and_validate(
                "post",
                "/users/sign_in",
                AuthenticateViaCredentialsLegacyResponse,
                json={
                    "sessions": {
                        "email": email,
                        "password": password,
                    }
                },
            )
        )

        self.user_uuid = auth_response.users.uuid
        self._access_token = auth_response.session.authentication_token

    async def async_request(
        self,
        method: str,
        endpoint: str,
        *,
        refresh_request: bool = False,
        **kwargs: dict[str, Any],
    ) -> dict[str, Any]:
        """Make an API request.

        Args:
            method: An HTTP method.
            endpoint: A relative API endpoint.
            refresh_request: Whether this is a request to refresh the access token.
            **kwargs: Additional kwargs to send with the request.

        Returns:
            An API response payload.

        Raises:
            InvalidCredentialsError: Raised upon invalid credentials.
            RequestError: Raised upon an underlying HTTP error.
        """
        if self._access_token_expires_at and utcnow() >= self._access_token_expires_at:
            LOGGER.debug("Access token expired, refreshing...")
            self._access_token = None
            self._access_token_expires_at = None
            await self.async_authenticate_from_refresh_token()

        # If an authenticated request arrives while we're refreshing, hold until the
        # refresh process is done:
        if not refresh_request and self._refreshing:
            await self._refresh_event.wait()

        url: str = f"{API_BASE}{endpoint}"

        kwargs.setdefault("headers", {})
        if self._access_token:
            kwargs["headers"]["Authorization"] = get_token_header_value(
                self._access_token, self._refresh_token
            )

        if use_running_session := self._session and not self._session.closed:
            session = self._session
        else:
            session = ClientSession(timeout=ClientTimeout(total=DEFAULT_TIMEOUT))

        data: dict[str, Any] = {}

        async with session.request(method, url, **kwargs) as resp:
            data = await resp.json()

            try:
                resp.raise_for_status()
            except ClientError as err:
                if "401" in str(err):
                    raise InvalidCredentialsError("Invalid credentials") from err
                raise RequestError(data["errors"][0]["title"]) from err

        if not use_running_session:
            await session.close()

        LOGGER.debug("Received data from %s: %s", endpoint, data)

        return data

    async def async_request_and_validate(
        self,
        method: str,
        endpoint: str,
        model: type[DataClassDictMixin],
        *,
        refresh_request: bool = False,
        **kwargs: dict[str, Any],
    ) -> NotionBaseModelT:
        """Make an API request and validate the response against a Pydantic model.

        Args:
            method: An HTTP method.
            endpoint: A relative API endpoint.
            model: A Pydantic model to validate the response against.
            refresh_request: Whether this is a request to refresh the access token.
            **kwargs: Additional kwargs to send with the request.

        Returns:
            A parsed, validated Pydantic model representing the response.
        """
        raw_data = await self.async_request(
            method, endpoint, refresh_request=refresh_request, **kwargs
        )

        try:
            return cast(NotionBaseModelT, model.from_dict(raw_data))
        except (
            MissingField,
            SuitableVariantNotFoundError,
            UnserializableDataError,
        ) as err:
            raise RequestError(
                f"Error while parsing response from {endpoint}: {err}"
            ) from err


async def async_get_client_with_credentials(
    email: str,
    password: str,
    *,
    session: ClientSession | None = None,
    session_name: str | None = None,
    use_legacy_auth: bool = False,
) -> Client:
    """Return an authenticated API object (using username/password)

    Args:
        email: The email address of a Notion account.
        password: The account password.
        session: An optional aiohttp ClientSession.
        session_name: An optional session name to use for authentication.
        use_legacy_auth: Whether to use the legacy authentication endpoint.

    Returns:
        An authenticated Client object.
    """
    client = Client(session=session, session_name=session_name)
    if use_legacy_auth:
        await client.async_legacy_authenticate_from_credentials(email, password)
    else:
        await client.async_authenticate_from_credentials(email, password)
    return client


# Alias for backwards compatibility:
async_get_client = async_get_client_with_credentials


async def async_get_client_with_refresh_token(
    user_uuid: str,
    refresh_token: str,
    *,
    session: ClientSession | None = None,
    session_name: str | None = None,
) -> Client:
    """Return an authenticated API object (using a refresh token).

    Args:
        user_uuid: The UUID of the user.
        refresh_token: A refresh token.
        session: An optional aiohttp ClientSession.
        session_name: An optional session name to use for authentication.

    Returns:
        An authenticated Client object.
    """
    client = Client(session=session, session_name=session_name)
    client.user_uuid = user_uuid
    await client.async_authenticate_from_refresh_token(refresh_token=refresh_token)
    return client
