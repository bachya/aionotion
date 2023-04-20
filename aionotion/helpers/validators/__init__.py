"""Define Pydantic validators."""
from __future__ import annotations

from datetime import datetime


def validate_timestamp(value: str | None) -> datetime | None:
    """Validate a timestamp.

    Args:
        value: An ISO 8601-formatted timestamp string.

    Returns:
        A parsed datetime.datetime object (UTC).
    """
    if not value:
        return None
    return datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f%z")
