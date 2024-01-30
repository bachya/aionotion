"""Define sensor models."""
# pylint: disable=consider-alternative-union-syntax
from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Literal, Optional

from pydantic import ConfigDict, Field, field_validator

from aionotion.const import LOGGER
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

    sensors: list[Sensor] = Field(alias="sensors")


class SensorGetResponse(NotionBaseModel):
    """Define an API response containing a single sensor."""

    sensor: Sensor = Field(alias="sensors")


class ListenerStatus(NotionBaseModel, extra="allow"):
    """Define a listener status."""

    trigger_value: str
    data_received_at: datetime

    validate_data_received_at = field_validator("data_received_at", mode="before")(
        validate_timestamp
    )


class ListenerLocalizedStatus(NotionBaseModel):
    """Define a localized listener status."""

    state: str
    description: str


class InsightOrigin(NotionBaseModel):
    """Define an insight origin."""

    type: Optional[str]
    id: Optional[str]


class PrimaryListenerInsight(NotionBaseModel):
    """Define a primary listener insight."""

    origin: Optional[InsightOrigin]
    value: Optional[str]
    data_received_at: Optional[datetime]

    validate_data_received_at = field_validator("data_received_at", mode="before")(
        validate_timestamp
    )


class ListenerInsights(NotionBaseModel):
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
    VERTICAL_HINGED_WINDOW = 12
    GARAGE_DOOR = 13
    HORIZONTAL_HINGED_WINDOW = 16
    SLIDING_DOOR_OR_WINDOW = 32
    UNKNOWN = 99


class Listener(NotionBaseModel):
    """Define a listener."""

    model_config = ConfigDict(frozen=True, protected_namespaces=())

    id: str
    created_at: datetime
    model_version: str
    sensor_id: str
    insights: ListenerInsights
    configuration: dict[str, Any]
    pro_monitoring_status: Literal["eligible", "ineligible"]

    device_type: str = Field(alias="type")
    listener_kind: ListenerKind = Field(alias="definition_id")
    status: Optional[ListenerStatus] = None
    status_localized: Optional[ListenerLocalizedStatus] = None

    @field_validator("listener_kind", mode="before")
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
            LOGGER.warning("Received an unknown listener kind: %s", value)
            return ListenerKind.UNKNOWN

    validate_created_at = field_validator("created_at", mode="before")(
        validate_timestamp
    )


class ListenerAllResponse(NotionBaseModel):
    """Define an API response containing all listeners."""

    listeners: list[Listener]
