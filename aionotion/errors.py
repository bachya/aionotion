"""Define package errors."""


class NotionError(Exception):
    """Define a base error."""


class RequestError(NotionError):
    """Define an error related to invalid requests."""


class InvalidCredentialsError(NotionError):
    """Define an error for unauthenticated accounts."""
