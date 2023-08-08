"""Define system models."""
# pylint: disable=consider-alternative-union-syntax
from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import Field, field_validator

from aionotion.helpers.model import NotionBaseModel
from aionotion.helpers.validator import validate_timestamp


class System(NotionBaseModel):
    """Define a system."""

    uuid: str
    name: str
    mode: str
    partners: list[str]
    latitude: float
    longitude: float
    timezone_id: str
    created_at: datetime
    updated_at: datetime
    night_time_start: datetime
    night_time_end: datetime
    id: int
    locality: str
    postal_code: str
    administrative_area: str
    fire_number: str
    police_number: str
    emergency_number: str
    address: Optional[str]
    notion_pro_permit: Optional[str]

    validate_created_at = field_validator("created_at", mode="before")(
        validate_timestamp
    )
    validate_updated_at = field_validator("updated_at", mode="before")(
        validate_timestamp
    )
    validate_night_time_start = field_validator("night_time_start", mode="before")(
        validate_timestamp
    )
    validate_night_time_end = field_validator("night_time_end", mode="before")(
        validate_timestamp
    )


class SystemAllResponse(NotionBaseModel):
    """Define an API response containing all systems."""

    systems: list[System]


class SystemGetResponse(NotionBaseModel):
    """Define an API response containing a single system."""

    system: System = Field(alias="systems")
