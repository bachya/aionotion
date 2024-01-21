"""Define a base client for interacting with Notion."""
from __future__ import annotations

from datetime import datetime
from typing import Any, cast
from uuid import uuid4

from aiohttp import ClientSession, ClientTimeout
from aiohttp.client_exceptions import ClientError
from pydantic import ValidationError

from aionotion.bridge import Bridge
from aionotion.const import LOGGER
from aionotion.errors import InvalidCredentialsError, RequestError
from aionotion.helpers.model import NotionBaseModel, NotionBaseModelT
from aionotion.sensor import Sensor
from aionotion.system import System
from aionotion.user import User
from aionotion.user.models import (
    AuthenticateViaCredentialsResponse,
    AuthenticateViaRefreshTokenResponse,
)
from aionotion.util.auth import decode_jwt
from aionotion.util.dt import utc_from_timestamp, utcnow

API_BASE = "https://api.getnotion.com/api"
API_VERSION = "2"

DEFAULT_TIMEOUT = 10


class Client:  # pylint: disable=too-few-public-methods
    """Define the API object."""

    def __init__(self, *, session: ClientSession | None = None) -> None:
        """Initialize.

        Args:
            session: An optional aiohttp ClientSession.
        """
        self._access_token: str | None = None
        self._access_token_expires_at: datetime | None = None
        self._refresh_token: str | None = None
        self._refreshing_access_token = False
        self._session = session
        self._session_uuid = uuid4().hex
        self.user_uuid: str = ""

        self.bridge = Bridge(self)
        self.sensor = Sensor(self)
        self.system = System(self)
        self.user = User(self)

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
                json={
                    "auth": {
                        "email": email,
                        "password": password,
                        "session_name": self._session_uuid,
                    }
                },
            )
        )

        self.user_uuid = str(auth_response.user.id)
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

        if refresh_token:
            # If a refresh token is explicitly provided, use it:
            self._refresh_token = refresh_token

        assert self._refresh_token is not None

        auth_response: AuthenticateViaRefreshTokenResponse = (
            await self.async_request_and_validate(
                "post",
                f"/auth/{self.user_uuid}/refresh",
                AuthenticateViaRefreshTokenResponse,
                json={"auth": {"refresh_token": self._refresh_token}},
            )
        )
        self._save_tokens_from_auth_response(auth_response)

    async def async_request(
        self, method: str, endpoint: str, **kwargs: dict[str, Any]
    ) -> dict[str, Any]:
        """Make an API request.

        Args:
            method: An HTTP method.
            endpoint: A relative API endpoint.
            **kwargs: Additional kwargs to send with the request.

        Returns:
            An API response payload.

        Raises:
            InvalidCredentialsError: Raised upon invalid credentials.
            RequestError: Raised upon an underlying HTTP error.
        """
        if (
            not self._refreshing_access_token
            and self._access_token_expires_at
            and utcnow() >= self._access_token_expires_at
        ):
            LOGGER.debug("Access token expired, refreshing...")
            self._refreshing_access_token = True
            await self.async_authenticate_from_refresh_token()

        url: str = f"{API_BASE}{endpoint}"

        kwargs.setdefault("headers", {})
        kwargs["headers"]["Accept-Version"] = API_VERSION
        if self._access_token:
            kwargs["headers"]["Authorization"] = f"Bearer {self._access_token}"

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

        LOGGER.debug("Received data from /%s: %s", endpoint, data)

        return data

    async def async_request_and_validate(
        self,
        method: str,
        endpoint: str,
        model: type[NotionBaseModel],
        **kwargs: dict[str, Any],
    ) -> NotionBaseModelT:
        """Make an API request and validate the response against a Pydantic model.

        Args:
            method: An HTTP method.
            endpoint: A relative API endpoint.
            model: A Pydantic model to validate the response against.
            **kwargs: Additional kwargs to send with the request.

        Returns:
            A parsed, validated Pydantic model representing the response.
        """
        raw_data = await self.async_request(method, endpoint, **kwargs)

        try:
            return cast(NotionBaseModelT, model.model_validate(raw_data))
        except ValidationError as err:
            raise RequestError(
                f"Error while parsing response from {endpoint}: {err}"
            ) from err


async def async_get_client(
    email: str, password: str, *, session: ClientSession | None = None
) -> Client:
    """Return an authenticated API object.

    Args:
        email: The email address of a Notion account.
        password: The account password.
        session: An optional aiohttp ClientSession.

    Returns:
        An authenticated Client object.
    """
    client = Client(session=session)
    await client.async_authenticate_from_credentials(email, password)
    return client
