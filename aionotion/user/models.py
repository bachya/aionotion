"""Define user models."""
from __future__ import annotations

from aionotion.helpers.model import NotionBaseModel


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
