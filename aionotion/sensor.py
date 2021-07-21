"""Define endpoints for interacting with sensors."""
from typing import Any, Callable, Dict, List


class Sensor:
    """Define an object to interact with all endpoints."""

    def __init__(self, request: Callable) -> None:
        """Initialize."""
        self._request = request

    async def async_all(self) -> List[Dict[str, Any]]:
        """Get all sensors."""
        resp: dict = await self._request("get", "sensors")
        return resp["sensors"]

    async def async_create(self, attributes: Dict[str, Any]) -> Dict[str, Any]:
        """Create a sensor with a specific attribute payload."""
        resp: dict = await self._request(
            "post", "sensors", json={"sensors": attributes}
        )
        return resp["sensors"]

    async def async_delete(self, sensor_id: int) -> None:
        """Delete a sensor by ID."""
        await self._request("delete", f"sensors/{sensor_id}")

    async def async_get(self, sensor_id: int) -> Dict[str, Any]:
        """Get a sensor by ID."""
        resp: dict = await self._request("get", f"sensors/{sensor_id}")
        return resp["sensors"]

    async def async_update(
        self, sensor_id: int, new_attributes: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update a sensor with a specific attribute payload."""
        resp: dict = await self._request(
            "put", f"sensors/{sensor_id}", json={"sensors": new_attributes}
        )
        return resp["sensors"]
