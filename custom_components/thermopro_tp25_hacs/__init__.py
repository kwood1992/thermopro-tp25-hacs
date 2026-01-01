"""TP25 Home Assistant integration."""

from __future__ import annotations

from bleak.exc import BleakError
from homeassistant.components import bluetooth
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from thermopro_tp25_ble import ThermoProTP25

from .const import _LOGGER, PLATFORMS
from .coordinator import ThermoProConfigEntry, ThermoProUpdateCoordinator


async def async_setup_entry(hass: HomeAssistant, entry: ThermoProConfigEntry) -> bool:
    """Set up Hello World from a config entry."""
    address = entry.data["address"]

    # Ensure a Bluetooth scanner exists
    bluetooth.async_get_scanner(hass)

    connection = ThermoProTP25(address)
    try:
        await connection.connect()
    except (BleakError, TimeoutError) as ex:
        await connection.disconnect()
        raise ConfigEntryNotReady(f"Could not connect to {address}: {ex}") from ex

    coordinator = ThermoProUpdateCoordinator(hass, entry, connection)
    try:
        await coordinator.async_config_entry_first_refresh()
    except ConfigEntryNotReady:
        await connection.disconnect()
        raise

    entry.runtime_data = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    coordinator = entry.runtime_data
    connection = coordinator.connection if coordinator else None

    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    if unload_ok and connection:
        connection.remove_callback(coordinator.unsub)

        try:
            await connection.disconnect()
        except Exception as ex:
            _LOGGER.exception(f"Error disconnecting from device: {ex}")

    entry.runtime_data = None

    return unload_ok
