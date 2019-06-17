# 📟 aionotion: a Python3, asyncio-friendly library for Notion® Home Monitoring

[![Travis CI](https://travis-ci.org/bachya/aionotion.svg?branch=master)](https://travis-ci.org/bachya/aionotion)
[![PyPi](https://img.shields.io/pypi/v/aionotion.svg)](https://pypi.python.org/pypi/aionotion)
[![Version](https://img.shields.io/pypi/pyversions/aionotion.svg)](https://pypi.python.org/pypi/aionotion)
[![License](https://img.shields.io/pypi/l/aionotion.svg)](https://github.com/bachya/aionotion/blob/master/LICENSE)
[![Code Coverage](https://codecov.io/gh/bachya/aionotion/branch/master/graph/badge.svg)](https://codecov.io/gh/bachya/aionotion)
[![Maintainability](https://api.codeclimate.com/v1/badges/bd79edca07c8e4529cba/maintainability)](https://codeclimate.com/github/bachya/aionotion/maintainability)
[![Say Thanks](https://img.shields.io/badge/SayThanks-!-1EAEDB.svg)](https://saythanks.io/to/bachya)

`aionotion` is a Python 3, asyncio-friendly library for interacting with
[Notion](https://getnotion.com) home monitoring sensors.

# Python Versions

`aionotion` is currently supported on:

* Python 3.5
* Python 3.6
* Python 3.7

However, running the test suite currently requires Python 3.6 or higher; tests
run on Python 3.5 will fail.

# Installation

```python
pip install aionotion
```

# Usage

`aionotion` starts within an
[aiohttp](https://aiohttp.readthedocs.io/en/stable/) `ClientSession`:

```python
import asyncio

from aiohttp import ClientSession


async def main() -> None:
    """Create the aiohttp session and run the example."""
    async with ClientSession() as websession:
      # YOUR CODE HERE


asyncio.get_event_loop().run_until_complete(main())
```

Create a client and get to work:

```python
import asyncio

from aiohttp import ClientSession

from aionotion import async_get_client


async def main() -> None:
    """Create the aiohttp session and run the example."""
    async with ClientSession() as websession:
        # Create a Notion API client:
        client = await async_get_client('<EMAIL>', '<PASSWORD>', websession)

        # Get all "households" associated with the account:
        systems = await client.system.async_all()

        # Get all bridges associated with the account:
        bridges = await client.bridge.async_all()

        # Get a bridge by ID:
        bridge = await client.bridge.async_get(12345)

        # Create a bridge (with associated parameters):
        await client.bridge.async_create({"system_id": 13579, "name": "Test"})

        # Update a bridge with new parameters:
        await client.bridge.async_update(12345, {"name": "Test"})

        # Reset a bridge (deprovision its WiFi credentials):
        await client.bridge.async_reset(12345)

        # Delete a bridge by ID:
        await client.bridge.async_delete(12345)

        # Get all sensors associated with the account:
        sensors = await client.sensor.async_all()

        # Get all "tasks" (conditions monitored by sensors) associated with the account:
        tasks = await client.task.async_all()


asyncio.get_event_loop().run_until_complete(main())
```

Check out `example.py`, the tests, and the source files themselves for method
signatures and more examples.

# Contributing

1. [Check for open features/bugs](https://github.com/bachya/aionotion/issues)
  or [initiate a discussion on one](https://github.com/bachya/aionotion/issues/new).
2. [Fork the repository](https://github.com/bachya/aionotion/fork).
3. Install the dev environment: `make init`.
4. Enter the virtual environment: `pipenv shell`
5. Code your new feature or bug fix.
6. Write a test that covers your new functionality.
7. Run tests and ensure 100% code coverage: `make coverage`
8. Add yourself to `AUTHORS.md`.
9. Submit a pull request!
