"""Sensor entities for Heating Curve Simulator."""
from __future__ import annotations

from decimal import Decimal, ROUND_HALF_UP

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfTemperature
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.event import async_track_state_change_event

from .const import CONF_LEVEL, CONF_ROOM_SETPOINT, CONF_SLOPE, DOMAIN, OUTDOOR_TEMPERATURES
from .entity import HeatingCurveSimulatorEntity


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up sensor entities."""
    async_add_entities(
        HeatingCurveFlowTemperatureSensor(hass, entry.entry_id, outdoor_temp)
        for outdoor_temp in OUTDOOR_TEMPERATURES
    )


class HeatingCurveFlowTemperatureSensor(HeatingCurveSimulatorEntity, SensorEntity):
    """Calculated target flow temperature sensor."""

    _attr_should_poll = False
    _attr_icon = "mdi:radiator"
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS

    def __init__(self, hass: HomeAssistant, entry_id: str, outdoor_temperature: int) -> None:
        super().__init__(entry_id)
        self.hass = hass
        self._outdoor_temperature = outdoor_temperature
        self._attr_name = f"Soll Vorlauftemperatur bei {outdoor_temperature}°C Außentemperatur"
        self._attr_unique_id = f"{entry_id}_flow_temp_{self._sanitize(outdoor_temperature)}"
        self._tracked_entity_ids = [
            f"number.{DOMAIN}_neigung",
            f"number.{DOMAIN}_niveau",
            f"number.{DOMAIN}_raumtemperatur_soll",
        ]
        self._unsub = None

    async def async_added_to_hass(self) -> None:
        """Subscribe to number entity updates."""
        await super().async_added_to_hass()

        @callback
        def _handle_state_change(event):
            self.async_write_ha_state()

        self._unsub = async_track_state_change_event(
            self.hass,
            self._tracked_entity_ids,
            _handle_state_change,
        )

    async def async_will_remove_from_hass(self) -> None:
        """Unsubscribe listeners."""
        if self._unsub is not None:
            self._unsub()

    @property
    def native_value(self) -> float | None:
        """Return calculated target flow temperature."""
        slope = self._get_number_value("number.heating_curve_simulator_neigung")
        level = self._get_number_value("number.heating_curve_simulator_niveau")
        room_setpoint = self._get_number_value("number.heating_curve_simulator_raumtemperatur_soll")

        if slope is None or level is None or room_setpoint is None:
            return None

        dar = self._outdoor_temperature - room_setpoint
        result = room_setpoint + level - slope * dar * (
            1.4347 + 0.021 * dar + 247.9e-6 * dar * dar
        )
        return float(Decimal(str(result)).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP))

    @property
    def extra_state_attributes(self) -> dict:
        """Return sensor attributes."""
        slope = self._get_number_value("number.heating_curve_simulator_neigung")
        level = self._get_number_value("number.heating_curve_simulator_niveau")
        room_setpoint = self._get_number_value("number.heating_curve_simulator_raumtemperatur_soll")
        dar = None if room_setpoint is None else self._outdoor_temperature - room_setpoint
        return {
            "outdoor_temperature": self._outdoor_temperature,
            "dar": dar,
            CONF_SLOPE: slope,
            CONF_LEVEL: level,
            CONF_ROOM_SETPOINT: room_setpoint,
            "formula": "room_setpoint + level - slope * dar * (1.4347 + 0.021 * dar + 247.9e-6 * dar * dar)",
        }

    def _get_number_value(self, entity_id: str) -> float | None:
        state = self.hass.states.get(entity_id)
        if state is None or state.state in ("unknown", "unavailable", None):
            return None
        try:
            return float(state.state)
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _sanitize(value: int) -> str:
        return f"minus_{abs(value)}" if value < 0 else str(value)
