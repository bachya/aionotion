"""Define fixtures for devices."""
import pytest


@pytest.fixture()
def device_all_json():
    """Define a response to GET /devices."""
    return {
        "devices": [
            {
                "id": 12345,
                "token": "123456abcde",
                "platform": "ios",
                "endpoint": "arn:aws:sns:us-west-2:307936840629:...",
                "created_at": "2019-06-17T00:57:09.937Z",
                "updated_at": "2019-06-17T00:57:09.937Z",
            }
        ]
    }


@pytest.fixture()
def device_create_json():
    """Define a response to POST /devices."""
    return {
        "devices": {
            "id": 12345,
            "token": "123456abcde",
            "platform": "ios",
            "endpoint": "arn:aws:sns:us-west-2:307936840629:...",
            "created_at": "2019-06-17T00:57:09.937Z",
            "updated_at": "2019-06-17T00:57:09.937Z",
        }
    }


@pytest.fixture()
def device_get_json():
    """Define a response to GET /devices/:id."""
    return {
        "devices": {
            "id": 12345,
            "token": "123456abcde",
            "platform": "ios",
            "endpoint": "arn:aws:sns:us-west-2:307936840629:...",
            "created_at": "2019-06-17T00:57:09.937Z",
            "updated_at": "2019-06-17T00:57:09.937Z",
        }
    }
