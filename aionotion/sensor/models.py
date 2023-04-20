"""Define sensor models."""
# pylint: disable=too-few-public-methods
from __future__ import annotations

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, validator

from aionotion.helpers.validators import validate_timestamp


class Bridge(BaseModel):
    """Define a bridge representation."""

    id: int
    hardware_id: str


class Firmware(BaseModel):
    """Define firmware information."""

    status: str


class SurfaceType(BaseModel):
    """Define a surface type."""

    id: str
    name: str
    slug: str


class User(BaseModel):
    """Define a user representation."""

    id: int
    email: str


class Sensor(BaseModel):
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
    installed_at: datetime
    calibrated_at: datetime
    last_reported_at: datetime
    missing_at: datetime | None
    updated_at: datetime
    created_at: datetime
    signal_strength: int
    firmware: Firmware
    surface_type: SurfaceType | None

    validate_installed_at = validator("installed_at", allow_reuse=True, pre=True)(
        validate_timestamp
    )
    validate_calibrated_at = validator("calibrated_at", allow_reuse=True, pre=True)(
        validate_timestamp
    )
    validate_last_reported_at = validator(
        "last_reported_at", allow_reuse=True, pre=True
    )(validate_timestamp)
    validate_missing_at = validator("missing_at", allow_reuse=True, pre=True)(
        validate_timestamp
    )
    validate_created_at = validator("created_at", allow_reuse=True, pre=True)(
        validate_timestamp
    )
    validate_updated_at = validator("updated_at", allow_reuse=True, pre=True)(
        validate_timestamp
    )


class SensorAllResponse(BaseModel):
    """Define an API response containing all sensors."""

    sensors: list[Sensor]


class SensorGetResponse(BaseModel):
    """Define an API response containing a single sensor."""

    sensor: Sensor

    class Config:
        """Define model configuration."""

        fields = {
            "sensor": "sensors",
        }


class ListenerStatus(BaseModel):
    """Define a listener status."""

    trigger_value: str
    data_received_at: datetime

    validate_data_received_at = validator(
        "data_received_at", allow_reuse=True, pre=True
    )(validate_timestamp)


class ListenerLocalizedStatus(BaseModel):
    """Define a localized listener status."""

    state: str
    description: str


class InsightOrigin(BaseModel):
    """Define an insight origin."""

    type: str | None
    id: str | None


class PrimaryListenerInsight(BaseModel):
    """Define a primary listener insight."""

    origin: InsightOrigin | None
    value: str | None
    data_received_at: datetime | None

    validate_data_received_at = validator(
        "data_received_at", allow_reuse=True, pre=True
    )(validate_timestamp)


class ListenerInsights(BaseModel):
    """Define listener insights:"""

    primary: PrimaryListenerInsight


class Listener(BaseModel):
    """Define a listener."""

    id: str
    definition_id: int
    created_at: datetime
    type: str
    model_version: str
    sensor_id: str
    status: ListenerStatus
    status_localized: ListenerLocalizedStatus
    insights: ListenerInsights
    configuration: dict[str, Any]
    pro_monitoring_status: Literal["eligible", "ineligible"]

    validate_created_at = validator("created_at", allow_reuse=True, pre=True)(
        validate_timestamp
    )


class ListenerAllResponse(BaseModel):
    """Define an API response containing all listeners."""

    listeners: list[Listener]
