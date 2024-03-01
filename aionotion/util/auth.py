"""Define auth utilities."""

from typing import Any

import jwt


def decode_jwt(encoded_jwt: str) -> dict[str, Any]:
    """Decode and return a JWT.

    Args:
        encoded_jwt: An encoded JWT.

    Returns:
        A decoded JWT.
    """
    return jwt.decode(
        encoded_jwt,
        "secret",
        algorithms=["HS256"],
        options={"verify_signature": False},
    )
