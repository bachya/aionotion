# 📟 aionotion: a Python3, asyncio-friendly library for Notion® Home Monitoring

[![CI][ci-badge]][ci]
[![PyPI][pypi-badge]][pypi]
[![Version][version-badge]][version]
[![License][license-badge]][license]
[![Code Coverage][codecov-badge]][codecov]
[![Maintainability][maintainability-badge]][maintainability]

<a href="https://www.buymeacoffee.com/bachya1208P" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="41" width="174"></a>

`aionotion` is a Python 3, asyncio-friendly library for interacting with [Notion][notion]
home monitoring sensors.

- [Installation](#installation)
- [Python Versions](#python-versions)
- [Usage](#usage)
- [Contributing](#contributing)

# Installation

```bash
pip install aionotion
```

# Python Versions

`aionotion` is currently supported on:

- Python 3.10
- Python 3.11
- Python 3.12

# Usage

```python
import asyncio

from aiohttp import ClientSession

from aionotion import async_get_client_with_credentials


async def main() -> None:
    """Create the aiohttp session and run the example."""
    client = await async_get_client_with_credentials(
        "<EMAIL>", "<PASSWORD>", session=session
    )

    # Get the UUID of the authenticated user:
    client.user_uuid
    # >>> xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx

    # Get the current refresh token of the authenticated user (BE CAREFUL):
    client.refresh_token
    # >>> abcde12345

    # Get all "households" associated with the account:
    systems = await client.system.async_all()
    # >>> [System(...), System(...), ...]

    # Get a system by ID:
    system = await client.system.async_get(12345)
    # >>> System(...)

    # Get all bridges associated with the account:
    bridges = await client.bridge.async_all()
    # >>> [Bridge(...), Bridge(...), ...]

    # Get a bridge by ID:
    bridge = await client.bridge.async_get(12345)
    # >>> Bridge(...)

    # Get all sensors:
    sensors = await client.sensor.async_all()
    # >>> [Sensor(...), Sensor(...), ...]

    # Get a sensor by ID:
    sensor = await client.sensor.async_get(12345)
    # >>> Sensor(...)

    # Get "listeners" (conditions that a sensor is monitoring) for all sensors:
    listeners = await client.listener.async_all()
    # >>> [Listener(...), Listener(...), ...]

    # Get all listener definitions supported by Notion:
    definitions = await client.listener.async_definitions()
    # >>> [ListenerDefinition(...), ListenerDefinition(...), ...]

    # Get user info:
    user_info = await client.user.async_info()
    # >>> User(...)

    # Get user preferences:
    user_preferences = await client.user.async_preferences()
    # >>> UserPreferences(...)


asyncio.run(main())
```

## Using a Refresh Token

During the normal course of operations, `aionotion` will automatically maintain a refresh
token and use it when needed. At times, you may wish to manage that token yourself (so
that you can use it later)–`aionotion` provides a few useful capabilities there.

### Refresh Token Callbacks

`aionotion` allows implementers to defining callbacks that get called when a new refresh
token is generated. These callbacks accept a single string parameter (the refresh
token):

```python
import asyncio

from aiohttp import ClientSession

from aionotion import async_get_client_with_credentials


async def main() -> None:
    """Create the aiohttp session and run the example."""
    client = await async_get_client_with_credentials(
        "<EMAIL>", "<PASSWORD>", session=session
    )

    def do_somethng_with_refresh_token(refresh_token: str) -> None:
        """Do something interesting."""
        pass

    # Attach the callback to the client:
    remove_callback = client.add_refresh_token_callback(do_somethng_with_refresh_token)

    # Later, if you want to remove the callback:
    remove_callback()


asyncio.run(main())
```

### Getting a Client via a Refresh Token

All of previous examples retrieved an authenticated client with
`async_get_client_with_credentials`. However, implementers may also create an
authenticated client by providing a previously retrieved user UUID and refresh token:

```python
import asyncio

from aiohttp import ClientSession

from aionotion import async_get_client_with_refresh_token


async def main() -> None:
    """Create the aiohttp session and run the example."""
    async with ClientSession() as session:
        # Create a Notion API client:
        client = await async_get_client_with_refresh_token(
            "<USER UUID>", "<REFRESH TOKEN>", session=session
        )

        # Get to work...


asyncio.run(main())
```

## Connection Pooling

By default, the library creates a new connection to Notion with each coroutine. If you
are calling a large number of coroutines (or merely want to squeeze out every second of
runtime savings possible), an [`aiohttp`][aiohttp] `ClientSession` can be used for
connection pooling:

```python
import asyncio

from aiohttp import ClientSession

from aionotion import async_get_client_with_credentials


async def main() -> None:
    """Create the aiohttp session and run the example."""
    async with ClientSession() as session:
        # Create a Notion API client:
        client = await async_get_client_with_credentials(
            "<EMAIL>", "<PASSWORD>", session=session
        )

        # Get to work...


asyncio.run(main())
```

Check out the examples, the tests, and the source files themselves for method
signatures and more examples.

# Contributing

Thanks to all of [our contributors][contributors] so far!

1. [Check for open features/bugs][issues] or [initiate a discussion on one][new-issue].
2. [Fork the repository][fork].
3. (_optional, but highly recommended_) Create a virtual environment: `python3 -m venv .venv`
4. (_optional, but highly recommended_) Enter the virtual environment: `source ./.venv/bin/activate`
5. Install the dev environment: `script/setup`
6. Code your new feature or bug fix on a new branch.
7. Write tests that cover your new functionality.
8. Run tests and ensure 100% code coverage: `poetry run pytest --cov aionotion tests`
9. Update `README.md` with any new documentation.
10. Submit a pull request!

[aiohttp]: https://github.com/aio-libs/aiohttp
[ci-badge]: https://img.shields.io/github/actions/workflow/status/bachya/aionotion/test.yml
[ci]: https://github.com/bachya/aionotion/actions
[codecov-badge]: https://codecov.io/gh/bachya/aionotion/branch/dev/graph/badge.svg
[codecov]: https://codecov.io/gh/bachya/aionotion
[contributors]: https://github.com/bachya/aionotion/graphs/contributors
[fork]: https://github.com/bachya/aionotion/fork
[issues]: https://github.com/bachya/aionotion/issues
[license-badge]: https://img.shields.io/pypi/l/aionotion.svg
[license]: https://github.com/bachya/aionotion/blob/main/LICENSE
[maintainability-badge]: https://api.codeclimate.com/v1/badges/bd79edca07c8e4529cba/maintainability
[maintainability]: https://codeclimate.com/github/bachya/aionotion/maintainability
[new-issue]: https://github.com/bachya/aionotion/issues/new
[notion]: https://getnotion.com
[pypi-badge]: https://img.shields.io/pypi/v/aionotion.svg
[pypi]: https://pypi.python.org/pypi/aionotion
[version-badge]: https://img.shields.io/pypi/pyversions/aionotion.svg
[version]: https://pypi.python.org/pypi/aionotion
