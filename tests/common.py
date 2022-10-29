"""Define common test utilities."""
import os

TEST_EMAIL = "user@email.com"
TEST_PASSWORD = "password123"  # noqa: S105
TEST_TOKEN = "12345abcde"  # noqa: S105


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
