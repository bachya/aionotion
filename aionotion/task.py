"""Define endpoints for interacting with tasks (monitored conditions)."""
from datetime import datetime
from typing import Callable, List


class Task:  # pylint: disable=too-few-public-methods
    """Define an object to interact with all endpoints."""

    def __init__(self, request: Callable) -> None:
        """Initialize."""
        self._request = request

    async def async_all(self) -> list:
        """Get all tasks."""
        resp = await self._request("get", "tasks")
        return resp["tasks"]

    async def async_create(self, sensor_id: int, tasks: List[dict]) -> list:
        """Create new tasks based upon a list of attribute dicts."""
        resp = await self._request(
            "post",
            "sensors/{0}/tasks".format(sensor_id),
            json={"sensor_id": sensor_id, "tasks": tasks},
        )
        return resp["tasks"]

    async def async_delete(self, sensor_id: int, task_id: str) -> None:
        """Delete a task by ID."""
        await self._request(
            "delete", "sensors/{0}/tasks/{1}".format(sensor_id, task_id)
        )

    async def async_get(self, task_id: str) -> dict:
        """Get a task by ID."""
        resp = await self._request("get", "tasks/{0}".format(task_id))
        return resp["tasks"]

    async def async_history(
        self, task_id: str, data_before: datetime, data_after: datetime
    ) -> dict:
        """Get the history of a task's values between two datetimes."""
        resp = await self._request(
            "get",
            "tasks/{0}/data".format(task_id),
            params={
                "data_before": data_before.isoformat(),
                "data_after": data_after.isoformat(),
            },
        )
        return resp["task"]["data"]
