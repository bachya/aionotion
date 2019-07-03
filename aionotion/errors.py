"""Define package errors."""


class NotionError(Exception):
    """Define a base error."""

    pass


class RequestError(NotionError):
    """Define an error related to invalid requests."""

    pass


class InvalidCredentialsError(NotionError):
    """Define an error for unauthenticated accounts."""

    pass
