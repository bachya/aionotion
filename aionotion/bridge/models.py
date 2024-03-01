"""Define bridge models."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

import ciso8601
from mashumaro import DataClassDictMixin


@dataclass(frozen=True, kw_only=True)
class FirmwareVersion(DataClassDictMixin):
    """Define firmware version info."""

    wifi: str
    wifi_app: str
    silabs: str | None = None
    ti: str | None = None


@dataclass(frozen=True, kw_only=True)
class Bridge(DataClassDictMixin):
    """Define a bridge."""

    id: int
    name: str | None
    mode: str
    hardware_id: str
    hardware_revision: int
    firmware_version: FirmwareVersion
    missing_at: datetime | None = field(
        default=None, metadata={"deserialize": ciso8601.parse_datetime}
    )
    created_at: datetime = field(metadata={"deserialize": ciso8601.parse_datetime})
    updated_at: datetime = field(metadata={"deserialize": ciso8601.parse_datetime})
    system_id: int
    firmware: FirmwareVersion
    links: dict[str, int | str]


@dataclass(frozen=True, kw_only=True)
class BridgeAllResponse(DataClassDictMixin):
    """Define an API response containing all bridges."""

    base_stations: list[Bridge]


@dataclass(frozen=True, kw_only=True)
class BridgeGetResponse(DataClassDictMixin):
    """Define an API response containing a single bridge."""

    base_stations: Bridge
