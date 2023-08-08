"""Define bridge models."""
# pylint: disable=consider-alternative-union-syntax
from __future__ import annotations

from datetime import datetime
from typing import Optional, Union

from pydantic import Field, field_validator

from aionotion.helpers.model import NotionBaseModel
from aionotion.helpers.validator import validate_timestamp


class FirmwareVersion(NotionBaseModel):
    """Define firmware version info."""

    wifi: str
    wifi_app: str
    silabs: Optional[str] = None
    ti: Optional[str] = None


class Bridge(NotionBaseModel):
    """Define a bridge."""

    id: int
    name: Optional[str]
    mode: str
    hardware_id: str
    hardware_revision: int
    firmware_version: FirmwareVersion
    missing_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    system_id: int
    firmware: FirmwareVersion
    links: dict[str, Union[int, str]]

    validate_missing_at = field_validator("missing_at", mode="before")(
        validate_timestamp
    )
    validate_created_at = field_validator("created_at", mode="before")(
        validate_timestamp
    )
    validate_updated_at = field_validator("updated_at", mode="before")(
        validate_timestamp
    )


class BridgeAllResponse(NotionBaseModel):
    """Define an API response containing all bridges."""

    bridges: list[Bridge] = Field(alias="base_stations")


class BridgeGetResponse(NotionBaseModel):
    """Define an API response containing a single bridge."""

    bridge: Bridge = Field(alias="base_stations")
