"""Define user models."""
from __future__ import annotations

from datetime import datetime

from pydantic import field_validator

from aionotion.helpers.model import NotionBaseModel
from aionotion.helpers.validator import validate_timestamp


class AuthTokens(NotionBaseModel):
    """Define auth tokens."""

    jwt: str
    refresh_token: str


class LegacySession(NotionBaseModel):
    """Define a legacy Notion session."""

    user_id: str
    authentication_token: str


class LegacyUser(NotionBaseModel):
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
    created_at: datetime
    updated_at: datetime

    validate_created_at = field_validator("created_at", mode="before")(
        validate_timestamp
    )
    validate_updated_at = field_validator("updated_at", mode="before")(
        validate_timestamp
    )


class User(NotionBaseModel):
    """Define a Notion user."""

    id: int
    uuid: str
    first_name: str
    last_name: str
    email: str
    phone_number: str | None
    role: str
    organization: str
    created_at: datetime
    updated_at: datetime

    validate_created_at = field_validator("created_at", mode="before")(
        validate_timestamp
    )
    validate_updated_at = field_validator("updated_at", mode="before")(
        validate_timestamp
    )


class AuthenticateViaCredentialsResponse(NotionBaseModel):
    """Define an API response for authentication via credentials."""

    user: User
    auth: AuthTokens


class AuthenticateViaCredentialsLegacyResponse(NotionBaseModel):
    """Define an API response for authentication via credentials (legacy)."""

    users: LegacyUser
    session: LegacySession


class AuthenticateViaRefreshTokenResponse(NotionBaseModel):
    """Define an API response for authentication via refresh token."""

    auth: AuthTokens


class UserPreferences(NotionBaseModel):
    """Define user preferences."""

    user_id: int
    military_time_enabled: bool
    celsius_enabled: bool
    disconnect_alerts_enabled: bool
    home_away_alerts_enabled: bool
    battery_alerts_enabled: bool


class UserPreferencesResponse(NotionBaseModel):
    """Define an API response containing all devices."""

    user_preferences: UserPreferences
