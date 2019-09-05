"""Define endpoints for interacting with tasks (monitored conditions)."""
from datetime import datetime
from typing import Callable, List


class Task:
    """Define an object to interact with all endpoints."""

    def __init__(self, request: Callable) -> None:
        """Initialize."""
        self._request: Callable = request

    async def async_all(self) -> list:
        """Get all tasks."""
        resp: dict = await self._request("get", "tasks")
        return resp["tasks"]

    async def async_create(self, sensor_id: int, tasks: List[dict]) -> list:
        """Create new tasks based upon a list of attribute dicts."""
        resp: dict = await self._request(
            "post",
            f"sensors/{sensor_id}/tasks",
            json={"sensor_id": sensor_id, "tasks": tasks},
        )
        return resp["tasks"]

    async def async_delete(self, sensor_id: int, task_id: str) -> None:
        """Delete a task by ID."""
        await self._request("delete", f"sensors/{sensor_id}/tasks/{task_id}")

    async def async_get(self, task_id: str) -> dict:
        """Get a task by ID."""
        resp: dict = await self._request("get", f"tasks/{task_id}")
        return resp["tasks"]

    async def async_history(
        self, task_id: str, data_before: datetime, data_after: datetime
    ) -> dict:
        """Get the history of a task's values between two datetimes."""
        resp: dict = await self._request(
            "get",
            f"tasks/{task_id}/data",
            params={
                "data_before": data_before.isoformat(),
                "data_after": data_after.isoformat(),
            },
        )
        return resp["task"]["data"]
