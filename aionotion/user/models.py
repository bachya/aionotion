"""Define user models."""
# pylint: disable=too-few-public-methods
from __future__ import annotations

from pydantic.v1 import BaseModel


class UserPreferences(BaseModel):
    """Define user preferences."""

    user_id: int
    military_time_enabled: bool
    celsius_enabled: bool
    disconnect_alerts_enabled: bool
    home_away_alerts_enabled: bool
    battery_alerts_enabled: bool


class UserPreferencesResponse(BaseModel):
    """Define an API response containing all devices."""

    user_preferences: UserPreferences
