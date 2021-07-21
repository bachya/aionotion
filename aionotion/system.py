"""Define endpoints for interacting with systems (accounts)."""
from typing import Any, Callable, Dict, List, cast


class System:
    """Define an object to interact with all endpoints."""

    def __init__(self, request: Callable) -> None:
        """Initialize."""
        self._request = request

    async def async_all(self) -> List[Dict[str, Any]]:
        """Get all systems."""
        resp = await self._request("get", "systems")
        return cast(List[Dict[str, Any]], resp["systems"])

    async def async_create(self, attributes: Dict[str, Any]) -> Dict[str, Any]:
        """Create a system with a specific attribute payload."""
        resp = await self._request("post", "systems", json={"systems": attributes})
        return cast(Dict[str, Any], resp["systems"])

    async def async_delete(self, system_id: int) -> None:
        """Delete a system by ID."""
        await self._request("delete", f"systems/{system_id}")

    async def async_get(self, system_id: int) -> Dict[str, Any]:
        """Get a system by ID."""
        resp = await self._request("get", f"systems/{system_id}")
        return cast(Dict[str, Any], resp["systems"])

    async def async_update(
        self, system_id: int, new_attributes: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update a system with a specific attribute payload."""
        resp = await self._request(
            "put", f"systems/{system_id}", json={"systems": new_attributes}
        )
        return cast(Dict[str, Any], resp["systems"])
