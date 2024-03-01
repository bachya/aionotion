"""Run an example script to quickly test."""

import asyncio
import logging
import os

from aiohttp import ClientSession

from aionotion import async_get_client_with_credentials
from aionotion.errors import NotionError

_LOGGER = logging.getLogger()

EMAIL = os.environ.get("NOTION_EMAIL")
PASSWORD = os.environ.get("NOTION_PASSWORD")


async def main() -> None:
    """Create the aiohttp session and run the example."""
    logging.basicConfig(level=logging.INFO)

    if not EMAIL or not PASSWORD:
        _LOGGER.error(
            "No email or password set (use NOTION_EMAIL and NOTION_PASSWORD "
            "environment variables)"
        )
        return

    async with ClientSession() as session:
        try:
            client = await async_get_client_with_credentials(
                EMAIL, PASSWORD, session=session
            )

            bridges = await client.bridge.async_all()
            _LOGGER.info("BRIDGES: %s", bridges)
            _LOGGER.info("============================================================")

            sensors = await client.sensor.async_all()
            _LOGGER.info("SENSORS: %s", sensors)
            _LOGGER.info("============================================================")

            listeners = await client.listener.async_all()
            _LOGGER.info("LISTENERS: %s", listeners)
            _LOGGER.info("============================================================")

            listener_definitions = await client.listener.async_definitions()
            _LOGGER.info("LISTENER DEFINITIONS: %s", listener_definitions)
            _LOGGER.info("============================================================")

            systems = await client.system.async_all()
            _LOGGER.info("SYSTEMS: %s", systems)
            _LOGGER.info("============================================================")

            user_info = await client.user.async_info()
            _LOGGER.info("USER_INFO: %s", user_info)
            _LOGGER.info("============================================================")

            user_preferences = await client.user.async_preferences()
            _LOGGER.info("USER_PREFERENCES: %s", user_preferences)
            _LOGGER.info("============================================================")
        except NotionError as err:
            _LOGGER.error("There was an error: %s", err)


asyncio.run(main())
