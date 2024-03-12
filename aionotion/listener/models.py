"""Define sensor models."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Literal

import ciso8601
from mashumaro import DataClassDictMixin, field_options

from aionotion.const import LOGGER


@dataclass(frozen=True, kw_only=True)
class ListenerLocalizedStatus(DataClassDictMixin):
    """Define a localized listener status."""

    state: str
    description: str


@dataclass(frozen=True, kw_only=True)
class InsightOrigin(DataClassDictMixin):
    """Define an insight origin."""

    id: str | None = None
    type: str | None = None


@dataclass(frozen=True, kw_only=True)
class PrimaryListenerInsight(DataClassDictMixin):
    """Define a primary listener insight."""

    origin: InsightOrigin | None
    value: str | None
    data_received_at: datetime | None = field(
        default=None, metadata={"deserialize": ciso8601.parse_datetime}
    )


@dataclass(frozen=True, kw_only=True)
class ListenerInsights(DataClassDictMixin):
    """Define listener insights:"""

    primary: PrimaryListenerInsight


class ListenerKind(Enum):
    """Define the kinds of listener."""

    BATTERY = 0
    WATER_FLOW = 1
    MOLD = 2
    TEMPERATURE = 3
    LEAK = 4
    SAFE = 5
    DOOR = 6
    ALARM = 7
    SENSOR_CONNECTION = 10
    WINDOW_HINGED_VERTICAL = 12
    GARAGE_DOOR = 13
    WINDOW_HINGED_HORIZONTAL = 16
    SYSTEM_OCCPUANCY = 23
    SENSOR_FIRMWARE = 24
    BRIDGE_FIRMWARE = 25
    BRIDGE_CONNECTION = 26
    SLIDING_DOOR_OR_WINDOW = 32
    SYSTEM_USER_OCCUPANCY = 33
    ESCALATION = 34
    SYSTEM_STATUS = 35
    UNKNOWN = 99


@dataclass(frozen=True, kw_only=True)
class Listener(DataClassDictMixin):
    """Define a listener."""

    id: str
    definition_id: int
    created_at: datetime = field(metadata={"deserialize": ciso8601.parse_datetime})
    model_version: str
    sensor_id: str
    status_localized: ListenerLocalizedStatus
    insights: ListenerInsights
    configuration: dict[str, Any]
    pro_monitoring_status: Literal["eligible", "ineligible"]
    device_type: str = field(metadata=field_options(alias="type"))
    kind: ListenerKind = field(init=False)

    def __post_init__(self) -> None:
        """Perform post-init initialization."""
        try:
            object.__setattr__(self, "kind", ListenerKind(self.definition_id))
        except ValueError:
            LOGGER.info("Unknown listener kind: %s", self.definition_id)
            object.__setattr__(self, "kind", ListenerKind.UNKNOWN)


@dataclass(frozen=True, kw_only=True)
class ListenerAllResponse(DataClassDictMixin):
    """Define an API response containing all listeners."""

    listeners: list[Listener]


@dataclass(frozen=True, kw_only=True)
class ListenerDefinition(DataClassDictMixin):
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


@dataclass(frozen=True, kw_only=True)
class ListenerDefinitionResponse(DataClassDictMixin):
    """Define an API response containing all listener definitions."""

    listener_definitions: list[ListenerDefinition]
