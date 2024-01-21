"""Run an example script to quickly test."""
import asyncio
import logging

from aiohttp import ClientSession

from aionotion import async_get_client
from aionotion.errors import NotionError

_LOGGER = logging.getLogger()

EMAIL = "email@address.com"
PASSWORD = "password"  # noqa: S105


async def main() -> None:
    """Create the aiohttp session and run the example."""
    logging.basicConfig(level=logging.INFO)
    async with ClientSession() as session:
        try:
            client = await async_get_client(EMAIL, PASSWORD, session=session)

            bridges = await client.bridge.async_all()
            _LOGGER.info("BRIDGES: %s", bridges)

            sensors = await client.sensor.async_all()
            _LOGGER.info("SENSORS: %s", sensors)

            listeners = await client.sensor.async_listeners()
            _LOGGER.info("LISTENERS: %s", listeners)

            systems = await client.system.async_all()
            _LOGGER.info("SYSTEMS: %s", systems)
        except NotionError as err:
            _LOGGER.error("There was an error: %s", err)


asyncio.run(main())
