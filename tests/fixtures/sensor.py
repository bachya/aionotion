"""Define fixtures for sensors."""
import pytest

from ..const import TEST_EMAIL


@pytest.fixture()
def sensor_all_json():
    """Define a response to GET /sensors."""
    return {
        "sensors": [
            {
                "id": 123456,
                "uuid": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
                "user": {"id": 12345, "email": TEST_EMAIL},
                "bridge": {"id": 12345, "hardware_id": "0x1234567890abcdef"},
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
                "links": {"location": 123456},
                "lqi": 0,
                "rssi": -46,
                "surface_type": None,
            },
            {
                "id": 132462,
                "uuid": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
                "user": {"id": 12345, "email": TEST_EMAIL},
                "bridge": {"id": 12345, "hardware_id": "0x1234567890abcdef"},
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
                "links": {"location": 123456},
                "lqi": 0,
                "rssi": -30,
                "surface_type": None,
            },
        ]
    }


@pytest.fixture()
def sensor_create_json():
    """Define a response to POST /sensors."""
    return {
        "sensors": {
            "id": 123456,
            "uuid": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
            "user": {"id": 12345, "email": TEST_EMAIL},
            "bridge": {"id": 12345, "hardware_id": "0x1234567890abcdef"},
            "last_bridge_hardware_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
            "name": "New Sensor",
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
            "links": {"location": 123456},
            "lqi": 0,
            "rssi": -46,
            "surface_type": None,
        }
    }


@pytest.fixture()
def sensor_get_json():
    """Define a response to GET /sensors/:id."""
    return {
        "sensors": {
            "id": 123456,
            "uuid": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
            "user": {"id": 12345, "email": TEST_EMAIL},
            "bridge": {"id": 12345, "hardware_id": "0x1234567890abcdef"},
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
            "links": {"location": 123456},
            "lqi": 0,
            "rssi": -46,
            "surface_type": None,
        }
    }


@pytest.fixture()
def sensor_update_json():
    """Define a response to PUT /sensors/:id."""
    return {
        "sensors": {
            "id": 123456,
            "uuid": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
            "user": {"id": 12345, "email": TEST_EMAIL},
            "bridge": {"id": 12345, "hardware_id": "0x1234567890abcdef"},
            "last_bridge_hardware_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
            "name": "Updated Sensor Name",
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
            "links": {"location": 123456},
            "lqi": 0,
            "rssi": -46,
            "surface_type": None,
        }
    }
