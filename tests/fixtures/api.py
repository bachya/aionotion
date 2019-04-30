"""Define fixtures for testing the Notion API."""
import pytest

from ..const import TEST_EMAIL, TEST_TOKEN


@pytest.fixture()
def base_stations_json():
    """Define a response to /base_stations."""
    return {
        "base_stations": [{
            "id": 12345,
            "name": None,
            "mode": "home",
            "hardware_id": "0x1234567890abcdef",
            "hardware_revision": 4,
            "firmware_version": {
                "wifi": "0.121.0",
                "wifi_app": "3.3.0",
                "silabs": "1.0.1"
            },
            "missing_at": None,
            "created_at": "2019-04-30T01:43:50.497Z",
            "updated_at": "2019-04-30T01:44:43.749Z",
            "system_id": 12345,
            "firmware": {
                "wifi": "0.121.0",
                "wifi_app": "3.3.0",
                "silabs": "1.0.1"
            },
            "links": {
                "system": 12345
            }
        }]
    }


@pytest.fixture()
def sign_in_json():
    """Define a response to /users/sign_in."""
    return {
        "users": {
            "id": 12345,
            "uuid": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
            "first_name": "John",
            "last_name": "Doe",
            "email": TEST_EMAIL,
            "phone_number": None,
            "role": "user",
            "organization": "Notion User",
            "authentication_token": TEST_TOKEN,
            "created_at": "2019-04-30T01:35:03.781Z",
            "updated_at": "2019-04-30T17:40:21.030Z"
        },
        "session": {
            "user_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
            "authentication_token": TEST_TOKEN
        }
    }


@pytest.fixture()
def systems_json():
    """Define a response to /systems."""
    return {
        "systems": [{
            "id": 12345,
            "uuid": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
            "name": "Home",
            "mode": "home",
            "latitude": 40.6892494,
            "longitude": -74.0445004,
            "timezone_id": "America/New_York",
            "locality": "New York",
            "postal_code": "10004",
            "administrative_area": "New York",
            "fire_number": "(212) 363-3200",
            "police_number": "(212) 363-3200",
            "emergency_number": "(212) 363-3200",
            "night_time_start": "2019-05-01T04:00:00.000Z",
            "night_time_end": "2019-05-01T13:00:00.000Z",
            "created_at": "2019-04-30T01:35:21.870Z",
            "updated_at": "2019-04-30T01:35:23.723Z"
        }]
    }


@pytest.fixture()
def sensors_json():
    """Define a response to /sensors."""
    return {
        "sensors": [{
            "id": 123456,
            "uuid": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
            "user": {
                "id": 12345,
                "email": TEST_EMAIL
            },
            "bridge": {
                "id": 12345,
                "hardware_id": "0x1234567890abcdef"
            },
            "last_bridge_hardware_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
            "name": "Bathroom Sensor",
            "location_id": 123456,
            "system_id": 12345,
            "hardware_id": "0x1234567890abcdef",
            "firmware_version": "1.1.2",
            "hardware_revision": 5,
            "device_key": "0x1234567890abcdef",
            "encryption_key": True,
            "installed_at": "2019-04-30T01:57:34.443Z",
            "calibrated_at": "2019-04-30T01:57:35.651Z",
            "last_reported_at": "2019-04-30T02:20:04.821Z",
            "missing_at": None,
            "updated_at": "2019-04-30T01:57:36.129Z",
            "created_at": "2019-04-30T01:56:45.932Z",
            "signal_strength": 5,
            "links": {
                "location": 123456
            },
            "lqi": 0,
            "rssi": -46,
            "surface_type": None
        }, {
            "id": 132462,
            "uuid": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
            "user": {
                "id": 12345,
                "email": TEST_EMAIL
            },
            "bridge": {
                "id": 12345,
                "hardware_id": "0x1234567890abcdef"
            },
            "last_bridge_hardware_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
            "name": "Living Room Sensor",
            "location_id": 123456,
            "system_id": 12345,
            "hardware_id": "0x1234567890abcdef",
            "firmware_version": "1.1.2",
            "hardware_revision": 5,
            "device_key": "0x1234567890abcdef",
            "encryption_key": True,
            "installed_at": "2019-04-30T01:45:56.169Z",
            "calibrated_at": "2019-04-30T01:46:06.256Z",
            "last_reported_at": "2019-04-30T02:20:04.829Z",
            "missing_at": None,
            "updated_at": "2019-04-30T01:46:07.717Z",
            "created_at": "2019-04-30T01:45:14.148Z",
            "signal_strength": 5,
            "links": {
                "location": 123456
            },
            "lqi": 0,
            "rssi": -30,
            "surface_type": None
        }]
    }


@pytest.fixture()
def tasks_json():
    """Define a response to /tasks."""
    return {
        "tasks": [{
            "id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
            "task_type": "missing",
            "sensor_data": [],
            "status": {
                "value": "missing",
                "received_at": "2019-04-30T03:57:41.716Z"
            },
            "created_at": "2019-04-30T01:56:46.004Z",
            "updated_at": "2019-04-30T03:57:42.004Z",
            "sensor_id": 132470,
            "model_version": "2.0",
            "configuration": {},
            "links": {
                "sensor": 123456
            }
        }, {
            "id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
            "task_type": "leak",
            "sensor_data": [],
            "status": {
                "value": "no_leak",
                "received_at": "2019-04-30T01:57:31.206Z"
            },
            "created_at": "2019-04-30T01:57:31.206Z",
            "updated_at": "2019-04-30T01:57:31.268Z",
            "sensor_id": 132470,
            "model_version": "2.1",
            "configuration": {},
            "links": {
                "sensor": 123456
            }
        }, {
            "id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
            "task_type": "alarm",
            "sensor_data": [],
            "status": {
                "value": "no_alarm",
                "received_at": "2019-04-30T01:57:30.972Z"
            },
            "created_at": "2019-04-30T01:57:30.971Z",
            "updated_at": "2019-04-30T01:57:31.046Z",
            "sensor_id": 132470,
            "model_version": "3.0",
            "configuration": {},
            "links": {
                "sensor": 123456
            }
        }, {
            "id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
            "task_type": "low_battery",
            "sensor_data": [],
            "status": {
                "value": "battery_good",
                "received_at": "2019-04-30T01:56:45.955Z"
            },
            "created_at": "2019-04-30T01:56:45.955Z",
            "updated_at": "2019-04-30T01:56:45.974Z",
            "sensor_id": 132470,
            "model_version": "2.0",
            "configuration": {},
            "links": {
                "sensor": 123456
            }
        }, {
            "id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
            "task_type": "missing",
            "sensor_data": [],
            "status": {
                "value": "missing",
                "received_at": "2019-04-30T03:57:41.716Z"
            },
            "created_at": "2019-04-30T01:45:14.370Z",
            "updated_at": "2019-04-30T03:57:41.981Z",
            "sensor_id": 132462,
            "model_version": "2.0",
            "configuration": {},
            "links": {
                "sensor": 123456
            }
        }, {
            "id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
            "task_type": "temperature",
            "sensor_data": [],
            "status": {
                "value": "20.2838134765625",
                "received_at": "2019-04-30T03:43:34.765Z"
            },
            "created_at": "2019-04-30T01:45:51.868Z",
            "updated_at": "2019-04-30T01:45:51.930Z",
            "sensor_id": 132462,
            "model_version": "2.1",
            "configuration": {
                "lower": 15.56,
                "upper": 29.44,
                "offset": 0.0
            },
            "links": {
                "sensor": 123456
            }
        }, {
            "id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
            "task_type": "low_battery",
            "sensor_data": [],
            "status": {
                "value": "battery_good",
                "received_at": "2019-04-30T01:45:14.221Z"
            },
            "created_at": "2019-04-30T01:45:14.221Z",
            "updated_at": "2019-04-30T01:45:14.230Z",
            "sensor_id": 132462,
            "model_version": "2.0",
            "configuration": {},
            "links": {
                "sensor": 123456
            }
        }]
    }
