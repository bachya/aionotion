"""Define a base client for interacting with Notion."""
from __future__ import annotations

from typing import Any

from aiohttp import ClientSession, ClientTimeout
from aiohttp.client_exceptions import ClientError

from .bridge import Bridge
from .device import Device
from .errors import InvalidCredentialsError, RequestError
from .sensor import Sensor
from .system import System
from .task import Task

API_BASE: str = "https://api.getnotion.com/api"

DEFAULT_TIMEOUT: int = 10


class Client:  # pylint: disable=too-few-public-methods
    """Define the API object."""

    def __init__(self, *, session: ClientSession | None = None) -> None:
        """Initialize.

        Args:
            session: An optional aiohttp ClientSession.
        """
        self._session = session
        self._token: str | None = None

        self.bridge = Bridge(self._request)
        self.device = Device(self._request)
        self.sensor = Sensor(self._request)
        self.system = System(self._request)
        self.task = Task(self._request)

    async def _request(
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
        url: str = f"{API_BASE}/{endpoint}"

        kwargs.setdefault("headers", {})
        if self._token:
            kwargs["headers"]["Authorization"] = f"Token token={self._token}"

        if use_running_session := self._session and not self._session.closed:
            session = self._session
        else:
            session = ClientSession(timeout=ClientTimeout(total=DEFAULT_TIMEOUT))

        data: dict[str, Any] = {}

        try:
            async with session.request(method, url, **kwargs) as resp:
                data = await resp.json()
                resp.raise_for_status()
        except ClientError as err:
            if "401" in str(err):
                raise InvalidCredentialsError("Invalid credentials") from err
            raise RequestError(data["errors"][0]["title"]) from err
        finally:
            if not use_running_session:
                await session.close()

        return data

    async def async_authenticate(self, email: str, password: str) -> None:
        """Authenticate the user and retrieve an authentication token.

        Args:
            email: The email address of a Notion account.
            password: The account password.
        """
        auth_response = await self._request(
            "post",
            "users/sign_in",
            json={"sessions": {"email": email, "password": password}},
        )

        self._token = auth_response["session"]["authentication_token"]


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
    client: Client = Client(session=session)
    await client.async_authenticate(email, password)
    return client
