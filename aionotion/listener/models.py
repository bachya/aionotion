"""Define sensor models."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Literal

import ciso8601
from mashumaro import DataClassDictMixin, field_options


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

    origin: InsightOrigin
    value: str
    data_received_at: datetime = field(
        metadata={"deserialize": ciso8601.parse_datetime}
    )


@dataclass(frozen=True, kw_only=True)
class ListenerInsights(DataClassDictMixin):
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
