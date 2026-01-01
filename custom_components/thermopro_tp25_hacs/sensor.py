"""Sensor platform for TP25."""

from __future__ import annotations

from homeassistant.components.sensor import SensorEntity
from homeassistant.const import PERCENTAGE, UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.components.sensor import SensorDeviceClass

from .const import DOMAIN
from .coordinator import ThermoProUpdateCoordinator, ThermoProConfigEntry
from thermopro_tp25_ble import (
    ProbeInfo,
    BatteryInfo,
    ProbeReading,
    BatteryReading,
    ThermoProTP25,
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ThermoProConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up TP25 sensors."""
    coordinator = entry.runtime_data

    entities: list[SensorEntity] = []

    # Add probe sensors
    for probe in coordinator.data["probes"]:
        entities.append(TP25ProbeSensor(coordinator, probe))

    # Add battery sensor
    entities.append(TP25BatterySensor(coordinator, coordinator.data["battery"]))

    # Correct: do NOT await this, just call it
    async_add_entities(entities)


class TP25ProbeSensor(CoordinatorEntity, SensorEntity):
    """Sensor for a single temperature probe."""

    def __init__(
        self, coordinator: ThermoProUpdateCoordinator, probe: ProbeInfo
    ) -> None:
        """Initialize probe sensor."""
        super().__init__(coordinator)

        self.coordinator = coordinator
        self.probe = probe

        self._probe_id = self.probe.probe_id
        self._attr_unique_id = f"{self.probe.probe_id}"
        self._attr_name = f"{self.probe.name}"
        self._attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS

    @property
    def available(self) -> bool:
        """Return connected state."""
        return self.coordinator.data is not None and self.coordinator.data.get(
            "connected", False
        )

    @property
    def native_value(self) -> int | None:
        """Return current temperature."""
        probes: list[ProbeReading] = self.coordinator.data.get("probes", [])
        for p in probes:
            if p.probe_id == self._probe_id:
                return getattr(p, "temperature", None)
        return None

    @property
    def device_info(self) -> DeviceInfo:
        """Link this probe to the TP25 hub device."""
        return DeviceInfo(
            identifiers={(DOMAIN, self.coordinator.name)},
            name="ThermoPro TP25",
            manufacturer="ThermoPro",
            model="TP25",
        )


class TP25BatterySensor(CoordinatorEntity, SensorEntity):
    """Battery sensor."""

    _attr_device_class = SensorDeviceClass.BATTERY

    def __init__(
        self, coordinator: ThermoProUpdateCoordinator, battery: BatteryInfo
    ) -> None:
        """Initialize battery sensor."""
        super().__init__(coordinator)

        self.coordinator = coordinator
        self.battery = battery

        self._attr_unique_id = f"{self.battery.battery_id}"
        self._attr_name = f"{self.battery.name}"
        self._attr_native_unit_of_measurement = PERCENTAGE

    @property
    def available(self) -> bool:
        """Return connected state."""
        return self.coordinator.data is not None and self.coordinator.data.get(
            "connected", False
        )

    @property
    def native_value(self) -> int | None:
        """Return current battery level."""
        battery: BatteryReading = self.coordinator.data.get("battery", 0)
        return getattr(battery, "level", None)

    @property
    def device_info(self) -> DeviceInfo:
        """Link this probe to the TP25 hub device."""
        return DeviceInfo(
            identifiers={(DOMAIN, self.coordinator.name)},
            name="ThermoPro TP25",
            manufacturer="ThermoPro",
            model="TP25",
        )
