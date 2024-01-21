"""Define common test utilities."""
import os
from uuid import uuid4

import jwt

TEST_EMAIL = "user@email.com"
TEST_PASSWORD = "password123"  # noqa: S105
TEST_RTID = str(uuid4())
TEST_USER_ID = "12345"
TEST_USER_UUID = str(uuid4())


def generate_jwt(issued_at: float) -> bytes:
    """Generate a JWT.

    Args:
        issued_at: A timestamp at which the JWT is issued.

    Returns:
        The JWT string.
    """
    return jwt.encode(
        {
            "sub": TEST_USER_UUID,
            "roles": ["delete_system", "manage_users"],
            "rtid": TEST_RTID,
            "exp": issued_at + (60 * 15),
        },
        "secret",
        algorithm="HS256",
    )


def load_fixture(filename: str) -> str:
    """Load a fixture.

    Args:
        filename: The filename of the fixtures/ file to load.

    Returns:
        A string containing the contents of the file.
    """
    path = os.path.join(os.path.dirname(__file__), "fixtures", filename)
    with open(path, encoding="utf-8") as fptr:
        return fptr.read()
