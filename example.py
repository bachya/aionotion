"""Run an example script to quickly test."""
import asyncio
import logging

from aiohttp import ClientSession

from aionotion import async_get_client
from aionotion.errors import NotionError

_LOGGER = logging.getLogger()

EMAIL = 'bachya1208@gmail.com'
PASSWORD = 'izfy;QxfXsHdtKkm9D.qbZLBB'


async def main() -> None:
    """Create the aiohttp session and run the example."""
    logging.basicConfig(level=logging.INFO)
    async with ClientSession() as session:
        try:
            api = await async_get_client(EMAIL, PASSWORD, session)

            systems = await api.async_get_systems()
            _LOGGER.info('SYSTEMS: %s', systems)

            base_stations = await api.async_get_base_stations()
            _LOGGER.info('BASE STATIONS: %s', base_stations)

            sensors = await api.async_get_sensors()
            _LOGGER.info('SENSORS: %s', sensors)

            tasks = await api.async_get_tasks()
            _LOGGER.info('TASKS: %s', tasks)
        except NotionError as err:
            _LOGGER.error('There was an error: %s', err)


asyncio.get_event_loop().run_until_complete(main())
