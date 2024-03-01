"""Define system models."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

import ciso8601
from mashumaro import DataClassDictMixin


@dataclass(frozen=True, kw_only=True)
class System(DataClassDictMixin):
    """Define a system."""

    uuid: str
    name: str
    mode: str
    partners: list[str]
    latitude: float
    longitude: float
    timezone_id: str
    created_at: datetime = field(metadata={"deserialize": ciso8601.parse_datetime})
    updated_at: datetime = field(metadata={"deserialize": ciso8601.parse_datetime})
    night_time_start: datetime = field(
        metadata={"deserialize": ciso8601.parse_datetime}
    )
    night_time_end: datetime = field(metadata={"deserialize": ciso8601.parse_datetime})
    id: int
    locality: str
    postal_code: str
    administrative_area: str
    fire_number: str
    police_number: str
    emergency_number: str
    address: str | None
    notion_pro_permit: str | None


@dataclass(frozen=True, kw_only=True)
class SystemAllResponse(DataClassDictMixin):
    """Define an API response containing all systems."""

    systems: list[System]


@dataclass(frozen=True, kw_only=True)
class SystemGetResponse(DataClassDictMixin):
    """Define an API response containing a single system."""

    systems: System
