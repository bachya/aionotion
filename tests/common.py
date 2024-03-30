"""Define common test utilities."""

from pathlib import Path
from uuid import uuid4

import jwt

TEST_EMAIL = "user@email.com"
TEST_PASSWORD = "password123"  # noqa: S105
TEST_REFRESH_TOKEN = "abcde12345"  # noqa: S105
TEST_USER_UUID = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"


def generate_jwt(issued_at: float) -> bytes:
    """Generate a JWT.

    Args:
    ----
        issued_at: A timestamp at which the JWT is issued.

    Returns:
    -------
        The JWT string.

    """
    return jwt.encode(
        {
            "sub": TEST_USER_UUID,
            "roles": ["delete_system", "manage_users"],
            "rtid": str(uuid4()),
            "exp": issued_at + (60 * 15),
        },
        "secret",
        algorithm="HS256",
    )


def load_fixture(filename: str) -> str:
    """Load a fixture.

    Args:
    ----
        filename: The filename of the fixtures/ file to load.

    Returns:
    -------
        A string containing the contents of the file.

    """
    path = Path(f"{Path(__file__).parent}/fixtures/{filename}")
    with Path.open(path, encoding="utf-8") as fptr:
        return fptr.read()
