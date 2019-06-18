"""Define fixtures for tasks."""
import pytest


@pytest.fixture()
def task_all_json():
    """Define a response to GET /tasks."""
    return {
        "tasks": [
            {
                "id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
                "task_type": "missing",
                "sensor_data": [],
                "status": {
                    "value": "missing",
                    "received_at": "2019-04-30T03:57:41.716Z",
                },
                "created_at": "2019-04-30T01:56:46.004Z",
                "updated_at": "2019-04-30T03:57:42.004Z",
                "sensor_id": 132470,
                "model_version": "2.0",
                "configuration": {},
                "links": {"sensor": 123456},
            },
            {
                "id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
                "task_type": "leak",
                "sensor_data": [],
                "status": {
                    "value": "no_leak",
                    "received_at": "2019-04-30T01:57:31.206Z",
                },
                "created_at": "2019-04-30T01:57:31.206Z",
                "updated_at": "2019-04-30T01:57:31.268Z",
                "sensor_id": 132470,
                "model_version": "2.1",
                "configuration": {},
                "links": {"sensor": 123456},
            },
            {
                "id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
                "task_type": "alarm",
                "sensor_data": [],
                "status": {
                    "value": "no_alarm",
                    "received_at": "2019-04-30T01:57:30.972Z",
                },
                "created_at": "2019-04-30T01:57:30.971Z",
                "updated_at": "2019-04-30T01:57:31.046Z",
                "sensor_id": 132470,
                "model_version": "3.0",
                "configuration": {},
                "links": {"sensor": 123456},
            },
            {
                "id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
                "task_type": "low_battery",
                "sensor_data": [],
                "status": {
                    "value": "battery_good",
                    "received_at": "2019-04-30T01:56:45.955Z",
                },
                "created_at": "2019-04-30T01:56:45.955Z",
                "updated_at": "2019-04-30T01:56:45.974Z",
                "sensor_id": 132470,
                "model_version": "2.0",
                "configuration": {},
                "links": {"sensor": 123456},
            },
            {
                "id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
                "task_type": "missing",
                "sensor_data": [],
                "status": {
                    "value": "missing",
                    "received_at": "2019-04-30T03:57:41.716Z",
                },
                "created_at": "2019-04-30T01:45:14.370Z",
                "updated_at": "2019-04-30T03:57:41.981Z",
                "sensor_id": 132462,
                "model_version": "2.0",
                "configuration": {},
                "links": {"sensor": 123456},
            },
            {
                "id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
                "task_type": "temperature",
                "sensor_data": [],
                "status": {
                    "value": "20.2838134765625",
                    "received_at": "2019-04-30T03:43:34.765Z",
                },
                "created_at": "2019-04-30T01:45:51.868Z",
                "updated_at": "2019-04-30T01:45:51.930Z",
                "sensor_id": 132462,
                "model_version": "2.1",
                "configuration": {"lower": 15.56, "upper": 29.44, "offset": 0.0},
                "links": {"sensor": 123456},
            },
            {
                "id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
                "task_type": "low_battery",
                "sensor_data": [],
                "status": {
                    "value": "battery_good",
                    "received_at": "2019-04-30T01:45:14.221Z",
                },
                "created_at": "2019-04-30T01:45:14.221Z",
                "updated_at": "2019-04-30T01:45:14.230Z",
                "sensor_id": 132462,
                "model_version": "2.0",
                "configuration": {},
                "links": {"sensor": 123456},
            },
        ]
    }


@pytest.fixture()
def task_create_json():
    """Define a response to POST /sensors/:id/tasks."""
    return {
        "tasks": {
            "id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
            "task_type": "missing",
            "sensor_data": [],
            "status": {"value": "missing", "received_at": "2019-04-30T03:57:41.716Z"},
            "created_at": "2019-04-30T01:56:46.004Z",
            "updated_at": "2019-04-30T03:57:42.004Z",
            "sensor_id": 132470,
            "model_version": "2.0",
            "configuration": {},
            "links": {"sensor": 123456},
        }
    }


@pytest.fixture()
def task_get_json():
    """Define a response to GET /tasks/:id."""
    return {
        "tasks": {
            "id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
            "task_type": "missing",
            "sensor_data": [],
            "status": {"value": "missing", "received_at": "2019-04-30T03:57:41.716Z"},
            "created_at": "2019-04-30T01:56:46.004Z",
            "updated_at": "2019-04-30T03:57:42.004Z",
            "sensor_id": 132470,
            "model_version": "2.0",
            "configuration": {},
            "links": {"sensor": 123456},
        }
    }


@pytest.fixture()
def task_history_json():
    """Define a response to GET /tasks/:id/data."""
    return {
        "task": {
            "id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
            "task_type": "temperature",
            "data": [
                {"time": "2019-06-17T04:09:55.786Z", "value": "23"},
                {"time": "2019-06-17T04:19:46.950Z", "value": "23"},
                {"time": "2019-06-17T04:29:37.572Z", "value": "22"},
            ],
        }
    }
