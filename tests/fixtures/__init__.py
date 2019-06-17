"""Define fixtures for testing the Notion API."""
import pytest

from ..const import TEST_EMAIL, TEST_TOKEN


@pytest.fixture()
def auth_success_json():
    """Define a response to GET /users/sign_in."""
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
            "updated_at": "2019-04-30T17:40:21.030Z",
        },
        "session": {
            "user_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
            "authentication_token": TEST_TOKEN,
        },
    }


@pytest.fixture()
def bad_api_json():
    """Define a response to GET /bad_endpoint."""
    return {"errors": [{"title": "No records found"}]}
