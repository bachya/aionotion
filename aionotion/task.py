"""Define endpoints for interacting with tasks (monitored conditions)."""
from collections.abc import Awaitable, Callable
from datetime import datetime
from typing import Any, cast


class Task:
    """Define an object to interact with all endpoints."""

    def __init__(self, request: Callable[..., Awaitable[dict[str, Any]]]) -> None:
        """Initialize.

        Args:
            request: The request method from the Client object.
        """
        self._request = request

    async def async_all(self) -> list[dict[str, Any]]:
        """Get all tasks.

        Returns:
            An API response payload.
        """
        resp = await self._request("get", "tasks")
        return cast(list[dict[str, Any]], resp["tasks"])

    async def async_create(
        self, sensor_id: int, tasks: list[dict[str, Any]]
    ) -> dict[str, Any]:
        """Add new tasks to a sensor.

        Args:
            sensor_id: The sensor to add the new tasks to.
            tasks: The tasks to add.

        Returns:
            An API response payload.
        """
        resp = await self._request(
            "post",
            f"sensors/{sensor_id}/tasks",
            json={"sensor_id": sensor_id, "tasks": tasks},
        )
        return cast(dict[str, Any], resp["tasks"])

    async def async_delete(self, sensor_id: int, task_id: str) -> None:
        """Delete a task by ID.

        Args:
            sensor_id: The sensor that contains the task to be deleted.
            task_id: The ID of the task to delete.
        """
        await self._request("delete", f"sensors/{sensor_id}/tasks/{task_id}")

    async def async_get(self, task_id: str) -> dict[str, Any]:
        """Get a task by ID.

        Args:
            task_id: The ID of the task to get.

        Returns:
            An API response payload.
        """
        resp = await self._request("get", f"tasks/{task_id}")
        return cast(dict[str, Any], resp["tasks"])

    async def async_history(
        self, task_id: str, data_before: datetime, data_after: datetime
    ) -> dict[str, Any]:
        """Get the history of a task's values between two datetimes.

        Args:
            task_id: The ID of the task to get.
            data_before: The ending datetime to which data should be constrained.
            data_after: The beginning datetime to which data should be constrained.

        Returns:
            An API response payload.
        """
        resp = await self._request(
            "get",
            f"tasks/{task_id}/data",
            params={
                "data_before": data_before.isoformat(),
                "data_after": data_after.isoformat(),
            },
        )
        return cast(dict[str, Any], resp["task"]["data"])
