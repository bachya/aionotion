"""Define device models."""
from __future__ import annotations

from datetime import datetime

from pydantic import Field, field_validator

from aionotion.helpers.model import NotionBaseModel
from aionotion.helpers.validator import validate_timestamp


class Device(NotionBaseModel):
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


class DeviceAllResponse(NotionBaseModel):
    """Define an API response containing all devices."""

    devices: list[Device]


class DeviceGetResponse(NotionBaseModel):
    """Define an API response containing a single device."""

    device: Device = Field(alias="devices")
