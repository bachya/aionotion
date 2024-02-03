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


class ListenerLocalizedStatus(NotionBaseModel):
    """Define a localized listener status."""

    state: str
    description: str


class InsightOrigin(NotionBaseModel):
    """Define an insight origin."""

    id: Optional[str] = None
    type: Optional[str] = None


class PrimaryListenerInsight(NotionBaseModel):
    """Define a primary listener insight."""

    origin: InsightOrigin
    value: str
    data_received_at: datetime

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
    HINGED_WINDOW = 12
    GARAGE_DOOR = 13
    SLIDING_DOOR_OR_WINDOW = 32
    UNKNOWN = 99


class Listener(NotionBaseModel):
    """Define a listener."""

    model_config = ConfigDict(frozen=True, protected_namespaces=())

    id: str
    created_at: datetime
    model_version: str
    sensor_id: str
    status_localized: ListenerLocalizedStatus
    insights: ListenerInsights
    configuration: dict[str, Any]
    pro_monitoring_status: Literal["eligible", "ineligible"]

    device_type: str = Field(alias="type")
    listener_kind: ListenerKind = Field(alias="definition_id")

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


class ListenerDefinition(NotionBaseModel):
    """Define an API response containing all listener definitions."""

    id: int
    name: str
    conflict_type: str
    priority: int
    hidden: bool
    conflicting_types: list[str]
    resources: dict | None
    compatible_hardware_revisions: list[int]
    type: str


class ListenerDefinitionResponse(NotionBaseModel):
    """Define an API response containing all listener definitions."""

    listener_definitions: list[ListenerDefinition]
