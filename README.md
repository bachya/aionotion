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

from aionotion import async_get_client


async def main() -> None:
    """Create the aiohttp session and run the example."""
    client = await async_get_client("<EMAIL>", "<PASSWORD>", session=session)

    # Get all "households" associated with the account:
    response = await client.system.async_all()
    # >>> [System(...), System(...), ...]

    # Get a system by ID:
    response = await client.system.async_get(12345)
    # >>> System(...)

    # Create a system (with associated parameters):
    response = await client.system.async_create({"system_id": 12345, "name": "Test"})
    # >>> System(...)

    # Update a system with new parameters:
    response = await client.system.async_update(12345, {"name": "Test"})
    # >>> System(...)

    # Delete a system by ID:
    await client.system.async_delete(12345)

    # Get all bridges associated with the account:
    response = await client.bridge.async_all()
    # >>> [Bridge(...), Bridge(...), ...]

    # Get a bridge by ID:
    response = await client.bridge.async_get(12345)
    # >>> Bridge(...)

    # Create a bridge (with associated parameters):
    response = await client.bridge.async_create({"system_id": 12345, "name": "Test"})
    # >>> Bridge(...)

    # Update a bridge with new parameters:
    response = await client.bridge.async_update(12345, {"name": "Test"})
    # >>> Bridge(...)

    # Reset a bridge (deprovision its WiFi credentials):
    response = await client.bridge.async_reset(12345)
    # >>> Bridge(...)

    # Delete a bridge by ID:
    await client.bridge.async_delete(12345)

    # Get all devices associated with the account:
    response = await client.device.async_all()
    # >>> [Device(...), Device(...), ...]

    # Get a device by ID:
    response = await client.device.async_get(12345)
    # >>> Device(...)

    # Create a device (with associated parameters):
    response = await client.device.async_create({"id": 12345})
    # >>> Device(...)

    # Delete a device by ID:
    await client.device.async_delete(12345)

    # Get all sensors:
    response = await client.sensor.async_all()
    # >>> [Sensor(...), Sensor(...), ...]

    # Get a sensor by ID:
    response = await client.sensor.async_get(12345)
    # >>> Sensor(...)

    # Get "listeners" (conditions that a sensor is monitoring) for all sensors:
    response = await client.sensor.async_listeners()
    # >>> [Listener(...), Listener(...), ...]

    # Get "listeners" (conditions that a sensor is monitoring) for a specific sensor;
    # note that unlike other sensor endpoints, this one requires the sensor UUID, *not*
    # the sensor ID:
    response = await client.sensor.async_listeners_for_sensor(
        "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
    )
    # >>> [Listener(...), Listener(...), ...]

    # Create a sensor (with associated parameters):
    response = await client.sensor.async_create({"sensor_id": 12345, "name": "Test"})
    # >>> Sensor(...)

    # Update a sensor with new parameters:
    response = await client.sensor.async_update(12345, {"name": "Test"})
    # >>> Sensor(...)

    # Delete a sensor by ID:
    await client.sensor.async_delete(12345)

    # Get user preferences:
    user_preferences = await client.user.async_preferences()
    # >>> UserPreferencesResponse(...)


asyncio.run(main())
```

By default, the library creates a new connection to Notion with each coroutine. If you
are calling a large number of coroutines (or merely want to squeeze out every second of
runtime savings possible), an [`aiohttp`][aiohttp] `ClientSession` can be used for
connection pooling:

```python
import asyncio

from aiohttp import ClientSession

from aionotion import async_get_client


async def main() -> None:
    """Create the aiohttp session and run the example."""
    async with ClientSession() as session:
        # Create a Notion API client:
        client = await async_get_client("<EMAIL>", "<PASSWORD>", session=session)

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
[ci-badge]: https://github.com/bachya/aionotion/workflows/CI/badge.svg
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
