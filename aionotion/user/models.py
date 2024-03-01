"""Define user models."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

import ciso8601
from mashumaro import DataClassDictMixin


@dataclass(frozen=True, kw_only=True)
class AuthTokens(DataClassDictMixin):
    """Define auth tokens."""

    jwt: str
    refresh_token: str


@dataclass(frozen=True, kw_only=True)
class LegacySession(DataClassDictMixin):
    """Define a legacy Notion session."""

    user_id: str
    authentication_token: str


@dataclass(frozen=True, kw_only=True)
class LegacyUser(DataClassDictMixin):
    """Define a legacy Notion user."""

    id: int
    uuid: str
    first_name: str
    last_name: str
    email: str
    phone_number: str | None
    role: str
    organization: str
    authentication_token: str
    created_at: datetime = field(metadata={"deserialize": ciso8601.parse_datetime})
    updated_at: datetime = field(metadata={"deserialize": ciso8601.parse_datetime})


@dataclass(frozen=True, kw_only=True)
class User(DataClassDictMixin):
    """Define a Notion user."""

    id: int
    uuid: str
    first_name: str
    last_name: str
    email: str
    phone_number: str | None
    role: str
    organization: str
    created_at: datetime = field(metadata={"deserialize": ciso8601.parse_datetime})
    updated_at: datetime = field(metadata={"deserialize": ciso8601.parse_datetime})


@dataclass(frozen=True, kw_only=True)
class UserInformationResponse(DataClassDictMixin):
    """Define an API response containing user information."""

    users: User


@dataclass(frozen=True, kw_only=True)
class AuthenticateViaCredentialsResponse(DataClassDictMixin):
    """Define an API response for authentication via credentials."""

    user: User
    auth: AuthTokens


@dataclass(frozen=True, kw_only=True)
class AuthenticateViaCredentialsLegacyResponse(DataClassDictMixin):
    """Define an API response for authentication via credentials (legacy)."""

    users: LegacyUser
    session: LegacySession


@dataclass(frozen=True, kw_only=True)
class AuthenticateViaRefreshTokenResponse(DataClassDictMixin):
    """Define an API response for authentication via refresh token."""

    auth: AuthTokens


@dataclass(frozen=True, kw_only=True)
class UserPreferences(DataClassDictMixin):
    """Define user preferences."""

    user_id: int
    military_time_enabled: bool
    celsius_enabled: bool
    disconnect_alerts_enabled: bool
    home_away_alerts_enabled: bool
    battery_alerts_enabled: bool


@dataclass(frozen=True, kw_only=True)
class UserPreferencesResponse(DataClassDictMixin):
    """Define an API response containing all devices."""

    user_preferences: UserPreferences
