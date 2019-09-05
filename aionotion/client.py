"""Define a base client for interacting with Notion."""
from typing import Optional

from aiohttp import ClientSession
from aiohttp.client_exceptions import ClientError

from .bridge import Bridge
from .device import Device
from .errors import InvalidCredentialsError, RequestError
from .sensor import Sensor
from .system import System
from .task import Task

API_BASE: str = "https://api.getnotion.com/api"


class Client:  # pylint: disable=too-few-public-methods
    """Define the API object."""

    def __init__(self, session: ClientSession) -> None:
        """Initialize."""
        self._session: ClientSession = session
        self._token: Optional[str] = None

        self.bridge: Bridge = Bridge(self._request)
        self.device: Device = Device(self._request)
        self.sensor: Sensor = Sensor(self._request)
        self.system: System = System(self._request)
        self.task: Task = Task(self._request)

    async def _request(
        self,
        method: str,
        endpoint: str,
        *,
        headers: dict = None,
        params: dict = None,
        json: dict = None,
    ) -> dict:
        """Make a request the API.com."""
        url: str = f"{API_BASE}/{endpoint}"

        if not headers:
            headers = {}

        if self._token:
            headers["Authorization"] = f"Token token={self._token}"

        async with self._session.request(
            method, url, headers=headers, params=params, json=json
        ) as resp:
            data: dict = await resp.json(content_type=None)
            try:
                resp.raise_for_status()
                return data
            except ClientError as err:
                if "401" in str(err):
                    raise InvalidCredentialsError("Invalid credentials")
                raise RequestError(data["errors"][0]["title"])

    async def async_authenticate(self, email: str, password: str) -> None:
        """Authenticate the user and retrieve an authentication token."""
        auth_response: dict = await self._request(
            "post",
            "users/sign_in",
            json={"sessions": {"email": email, "password": password}},
        )

        self._token = auth_response["session"]["authentication_token"]


async def async_get_client(email: str, password: str, session: ClientSession) -> Client:
    """Return an authenticated API object."""
    client: Client = Client(session)
    await client.async_authenticate(email, password)
    return client
