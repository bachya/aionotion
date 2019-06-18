"""Define fixtures for systems."""
import pytest


@pytest.fixture()
def system_all_json():
    """Define a response to GET /systems."""
    return {
        "systems": [
            {
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
                "updated_at": "2019-04-30T01:35:23.723Z",
            }
        ]
    }


@pytest.fixture()
def system_create_json():
    """Define a response to POST /systems."""
    return {
        "systems": {
            "id": 12345,
            "uuid": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
            "name": "New System",
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
            "updated_at": "2019-04-30T01:35:23.723Z",
        }
    }


@pytest.fixture()
def system_get_json():
    """Define a response to GET /systems/:id."""
    return {
        "systems": {
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
            "updated_at": "2019-04-30T01:35:23.723Z",
        }
    }


@pytest.fixture()
def system_update_json():
    """Define a response to PUT /systems/:id."""
    return {
        "systems": {
            "id": 12345,
            "uuid": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
            "name": "Updated System Name",
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
            "updated_at": "2019-04-30T01:35:23.723Z",
        }
    }
