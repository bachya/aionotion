"""Define a base client for interacting with Notion."""
from typing import Optional

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
        self._session: ClientSession = session
        self._token: Optional[str] = None

        self.bridge: Bridge = Bridge(self._request)
        self.device: Device = Device(self._request)
        self.sensor: Sensor = Sensor(self._request)
        self.system: System = System(self._request)
        self.task: Task = Task(self._request)

    async def _request(self, method: str, endpoint: str, **kwargs) -> dict:
        """Make a request the API.com."""
        url: str = f"{API_BASE}/{endpoint}"

        kwargs.setdefault("headers", {})
        if self._token:
            kwargs["headers"]["Authorization"] = f"Token token={self._token}"

        use_running_session = self._session and not self._session.closed

        if use_running_session:
            session = self._session
        else:
            session = ClientSession(timeout=ClientTimeout(total=DEFAULT_TIMEOUT))

        try:
            async with session.request(method, url, **kwargs) as resp:
                data: dict = await resp.json(content_type=None)
                resp.raise_for_status()
                return data
        except ClientError as err:
            if "401" in str(err):
                raise InvalidCredentialsError("Invalid credentials") from err
            raise RequestError(data["errors"][0]["title"]) from err
        finally:
            if not use_running_session:
                await session.close()

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
