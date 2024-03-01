"""Define sensor models."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

import ciso8601
from mashumaro import DataClassDictMixin


@dataclass(frozen=True, kw_only=True)
class Bridge(DataClassDictMixin):
    """Define a bridge representation."""

    id: int
    hardware_id: str


@dataclass(frozen=True, kw_only=True)
class Firmware(DataClassDictMixin):
    """Define firmware information."""

    status: str


@dataclass(frozen=True, kw_only=True)
class SurfaceType(DataClassDictMixin):
    """Define a surface type."""

    id: str
    name: str
    slug: str


@dataclass(frozen=True, kw_only=True)
class User(DataClassDictMixin):
    """Define a user representation."""

    id: int
    email: str


@dataclass(frozen=True, kw_only=True)
class Sensor(DataClassDictMixin):  # pylint: disable=too-many-instance-attributes
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
    installed_at: datetime | None = field(
        default=None, metadata={"deserialize": ciso8601.parse_datetime}
    )
    calibrated_at: datetime | None = field(
        default=None, metadata={"deserialize": ciso8601.parse_datetime}
    )
    last_reported_at: datetime | None = field(
        default=None, metadata={"deserialize": ciso8601.parse_datetime}
    )
    missing_at: datetime | None = field(
        default=None, metadata={"deserialize": ciso8601.parse_datetime}
    )
    updated_at: datetime = field(metadata={"deserialize": ciso8601.parse_datetime})
    created_at: datetime = field(metadata={"deserialize": ciso8601.parse_datetime})
    signal_strength: int
    firmware: Firmware
    surface_type: SurfaceType | None


@dataclass(frozen=True, kw_only=True)
class SensorAllResponse(DataClassDictMixin):
    """Define an API response containing all sensors."""

    sensors: list[Sensor]


@dataclass(frozen=True, kw_only=True)
class SensorGetResponse(DataClassDictMixin):
    """Define an API response containing a single sensor."""

    sensors: Sensor
