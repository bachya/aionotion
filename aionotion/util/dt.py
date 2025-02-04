"""Define datetime utilities."""

from datetime import UTC, datetime


def utcnow() -> datetime:
    """Return the current UTC time.

    Returns
    -------
        A ``datetime.datetime`` object.

    """
    return datetime.now(tz=UTC)


def utc_from_timestamp(timestamp: float) -> datetime:
    """Return a UTC time from a timestamp.

    Args:
    ----
        timestamp: The epoch to convert.

    Returns:
    -------
        A parsed ``datetime.datetime`` object.

    """
    return datetime.fromtimestamp(timestamp, tz=UTC)
