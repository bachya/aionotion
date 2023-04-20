"""Define sensor models."""
# pylint: disable=consider-alternative-union-syntax,too-few-public-methods
from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Literal, Optional

from pydantic import BaseModel, Extra, validator

from aionotion.const import LOGGER
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
    missing_at: Optional[datetime]
    updated_at: datetime
    created_at: datetime
    signal_strength: int
    firmware: Firmware
    surface_type: Optional[SurfaceType]

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


class ListenerStatus(BaseModel, extra=Extra.allow):
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

    type: Optional[str]
    id: Optional[str]


class PrimaryListenerInsight(BaseModel):
    """Define a primary listener insight."""

    origin: Optional[InsightOrigin]
    value: Optional[str]
    data_received_at: Optional[datetime]

    validate_data_received_at = validator(
        "data_received_at", allow_reuse=True, pre=True
    )(validate_timestamp)


class ListenerInsights(BaseModel):
    """Define listener insights:"""

    primary: PrimaryListenerInsight


class ListenerKind(Enum):
    """Define the kinds of listener."""

    BATTERY = 0
    MOLD = 2
    TEMPERATURE = 3
    LEAK_STATUS = 4
    SAFE = 5
    DOOR = 6
    SMOKE = 7
    CONNECTED = 10
    HINGED_WINDOW = 12
    GARAGE_DOOR = 13
    SLIDING_DOOR_OR_WINDOW = 32
    UNKNOWN = 99


class Listener(BaseModel):
    """Define a listener."""

    id: str
    listener_kind: ListenerKind
    created_at: datetime
    device_type: str
    model_version: str
    sensor_id: str
    status: ListenerStatus
    status_localized: ListenerLocalizedStatus
    insights: ListenerInsights
    configuration: dict[str, Any]
    pro_monitoring_status: Literal["eligible", "ineligible"]

    @validator("listener_kind", pre=True)
    @classmethod
    def validate_listener_kind(cls, value: str) -> ListenerKind:
        """Validate the API key type.

        Args:
            value: An API key to validate.

        Returns:
            A parsed ApiKeyType.

        Raises:
            ValueError: An invalid API key type was received.
        """
        try:
            return ListenerKind(value)
        except ValueError:
            LOGGER.error("Received an unknown listener kind: %s", value)
            return ListenerKind.UNKNOWN

    validate_created_at = validator("created_at", allow_reuse=True, pre=True)(
        validate_timestamp
    )

    class Config:
        """Define model configuration."""

        fields = {
            "device_type": "type",
            "listener_kind": "definition_id",
        }


class ListenerAllResponse(BaseModel):
    """Define an API response containing all listeners."""

    listeners: list[Listener]
