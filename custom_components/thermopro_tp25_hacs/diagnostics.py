"""Diagnostics support for TP25."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN


async def async_get_config_entry_diagnostics(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> dict[str, object]:
    """Return diagnostics for a TP25 config entry."""
    coordinator = hass.data[DOMAIN][entry.entry_id]

    return {
        "address": coordinator.address,
        "connected": coordinator.data is not None,
        "latest_data": coordinator.data,
    }
