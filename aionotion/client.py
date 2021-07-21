"""Define a base client for interacting with Notion."""
from typing import Any, Dict, Optional

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

    def __init__(self, *, session: Optional[ClientSession] = None) -> None:
        """Initialize."""
        self._session: Optional[ClientSession] = session
        self._token: Optional[str] = None

        self.bridge = Bridge(self._request)
        self.device = Device(self._request)
        self.sensor = Sensor(self._request)
        self.system = System(self._request)
        self.task = Task(self._request)

    async def _request(
        self, method: str, endpoint: str, **kwargs: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Make an API request."""
        url: str = f"{API_BASE}/{endpoint}"

        kwargs.setdefault("headers", {})
        if self._token:
            kwargs["headers"]["Authorization"] = f"Token token={self._token}"

        use_running_session = self._session and not self._session.closed

        if use_running_session:
            session = self._session
        else:
            session = ClientSession(timeout=ClientTimeout(total=DEFAULT_TIMEOUT))

        assert session

        data: Dict[str, Any] = {}

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
        """Authenticate the user and retrieve an authentication token."""
        auth_response: dict = await self._request(
            "post",
            "users/sign_in",
            json={"sessions": {"email": email, "password": password}},
        )

        self._token = auth_response["session"]["authentication_token"]


async def async_get_client(
    email: str, password: str, *, session: Optional[ClientSession] = None
) -> Client:
    """Return an authenticated API object."""
    client: Client = Client(session=session)
    await client.async_authenticate(email, password)
    return client
