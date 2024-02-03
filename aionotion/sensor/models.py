"""Define sensor models."""
# pylint: disable=consider-alternative-union-syntax
from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import field_validator

from aionotion.helpers.model import NotionBaseModel
from aionotion.helpers.validator import validate_timestamp


class Bridge(NotionBaseModel):
    """Define a bridge representation."""

    id: int
    hardware_id: str


class Firmware(NotionBaseModel):
    """Define firmware information."""

    status: str


class SurfaceType(NotionBaseModel):
    """Define a surface type."""

    id: str
    name: str
    slug: str


class User(NotionBaseModel):
    """Define a user representation."""

    id: int
    email: str


class Sensor(NotionBaseModel):
    """Define a sensor."""

    id: int
    uuid: str
    user: User
    bridge: Bridge
    last_bridge_hardware_id: str
    name: str
    location_id: int
    system_id: int
    hardware_id: str
    hardware_revision: int
    firmware_version: str
    device_key: str
    encryption_key: bool
    installed_at: Optional[datetime]
    calibrated_at: Optional[datetime]
    last_reported_at: Optional[datetime]
    missing_at: Optional[datetime]
    updated_at: datetime
    created_at: datetime
    signal_strength: int
    firmware: Firmware
    surface_type: Optional[SurfaceType]

    validate_installed_at = field_validator("installed_at", mode="before")(
        validate_timestamp
    )
    validate_calibrated_at = field_validator("calibrated_at", mode="before")(
        validate_timestamp
    )
    validate_last_reported_at = field_validator("last_reported_at", mode="before")(
        validate_timestamp
    )
    validate_missing_at = field_validator("missing_at", mode="before")(
        validate_timestamp
    )
    validate_created_at = field_validator("created_at", mode="before")(
        validate_timestamp
    )
    validate_updated_at = field_validator("updated_at", mode="before")(
        validate_timestamp
    )


class SensorAllResponse(NotionBaseModel):
    """Define an API response containing all sensors."""

    sensors: list[Sensor]


class SensorGetResponse(NotionBaseModel):
    """Define an API response containing a single sensor."""

    sensors: Sensor
