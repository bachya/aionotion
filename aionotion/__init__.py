"""Define a base API for interacting with Notion."""
from typing import Optional

from aiohttp import ClientSession
from aiohttp.client_exceptions import ClientError

from .errors import RequestError

API_BASE = 'https://api.getnotion.com/api'


class API:
    """Define the API object."""

    def __init__(self, session: ClientSession) -> None:
        """Initialize."""
        self._session = session
        self._token = None  # type: Optional[str]

    async def _request(
            self,
            method: str,
            endpoint: str,
            *,
            headers: dict = None,
            params: dict = None,
            json: dict = None) -> dict:
        """Make a request the API.com."""
        url = '{0}/{1}'.format(API_BASE, endpoint)

        if not headers:
            headers = {}

        if self._token:
            headers['Authorization'] = 'Token token={0}'.format(self._token)

        async with self._session.request(method, url, headers=headers,
                                         params=params, json=json) as resp:
            try:
                resp.raise_for_status()
                return await resp.json(content_type=None)
            except ClientError as err:
                raise RequestError(
                    "Error requesting data from {0}: {1}".format(url, err))

    async def async_authenticate(self, email: str, password: str) -> None:
        """Authenticate the user and retrieve an authentication token."""
        auth_response = await self._request(
            'post',
            'users/sign_in',
            json={'sessions': {
                'email': email,
                'password': password
            }})

        self._token = auth_response['session']['authentication_token']

    async def async_get_base_stations(self):
        """Get all Notion base stations associated with the account."""
        resp = await self._request('get', 'base_stations')
        return resp['base_stations']

    async def async_get_sensors(self):
        """Get all Notion "households" associated with the account."""
        resp = await self._request('get', 'sensors')
        return resp['sensors']

    async def async_get_systems(self):
        """Get all Notion "households" associated with the account."""
        resp = await self._request('get', 'systems')
        return resp['systems']

    async def async_get_tasks(self):
        """Get all Notion "households" associated with the account."""
        resp = await self._request('get', 'tasks')
        return resp['tasks']


async def async_get_client(
        email: str, password: str, session: ClientSession) -> API:
    """Return an authenticated API object."""
    api = API(session)
    await api.async_authenticate(email, password)
    return api
