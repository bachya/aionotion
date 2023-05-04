"""Define bridge models."""
# pylint: disable=consider-alternative-union-syntax,too-few-public-methods
from __future__ import annotations

from datetime import datetime
from typing import Optional, Union

from pydantic import BaseModel, validator

from aionotion.helpers.validators import validate_timestamp


class FirmwareVersion(BaseModel):
    """Define firmware version info."""

    silabs: str
    wifi: str
    wifi_app: str


class Bridge(BaseModel):
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

    validate_missing_at = validator("missing_at", allow_reuse=True, pre=True)(
        validate_timestamp
    )
    validate_created_at = validator("created_at", allow_reuse=True, pre=True)(
        validate_timestamp
    )
    validate_updated_at = validator("updated_at", allow_reuse=True, pre=True)(
        validate_timestamp
    )


class BridgeAllResponse(BaseModel):
    """Define an API response containing all bridges."""

    bridges: list[Bridge]

    class Config:
        """Define model configuration."""

        fields = {
            "bridges": "base_stations",
        }


class BridgeGetResponse(BaseModel):
    """Define an API response containing a single bridge."""

    bridge: Bridge

    class Config:
        """Define model configuration."""

        fields = {
            "bridge": "base_stations",
        }
