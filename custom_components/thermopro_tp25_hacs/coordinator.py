"""Coordinator for ThermoPro TP25."""

from __future__ import annotations

from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from thermopro_tp25_ble import BatteryReading, ProbeReading, ThermoProTP25

from .const import _LOGGER

type ThermoProConfigEntry = ConfigEntry[ThermoProUpdateCoordinator]


class ThermoProUpdateCoordinator(DataUpdateCoordinator):
    """DataUpdateCoordinator to gather data for a specific ThermoPro TP25 device."""

    config_entry: ThermoProConfigEntry

    def __init__(
        self,
        hass: HomeAssistant,
        config_entry: ThermoProConfigEntry,
        connection: ThermoProTP25,
    ) -> None:
        """Initialise DataUpdateCoordinator."""
        self.connection = connection
        self.device = connection.address

        super().__init__(
            hass, _LOGGER, config_entry=config_entry, name=f"{self.device}"
        )

        self.unsub = self.connection.register_callback(self._handle_push)

    async def _async_update_data(self) -> dict[str, Any]:
        return {
            "connected": self.connection.connected,
            "probes": self.connection.probes,
            "battery": self.connection.battery,
        }

    def _handle_push(
        self, connected: bool, probes: list[ProbeReading], battery: BatteryReading
    ) -> None:
        """Receive push updates from the hub and notify coordinator."""
        self.data = {
            "connected": connected,
            "probes": probes,
            "battery": battery,
        }
        self.async_set_updated_data(self.data)
