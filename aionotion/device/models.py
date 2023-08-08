"""Define device models."""
# pylint: disable=too-few-public-methods
from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, field_validator

from aionotion.helpers.validators import validate_timestamp


class Device(BaseModel):
    """Define a device."""

    id: int
    token: str
    platform: str
    endpoint: str
    created_at: datetime
    updated_at: datetime

    validate_created_at = field_validator("created_at", mode="before")(
        validate_timestamp
    )
    validate_updated_at = field_validator("updated_at", mode="before")(
        validate_timestamp
    )


class DeviceAllResponse(BaseModel):
    """Define an API response containing all devices."""

    devices: list[Device]


class DeviceGetResponse(BaseModel):
    """Define an API response containing a single device."""

    device: Device
    model_config = {
        "fields": {
            "device": "device",
        }
    }
