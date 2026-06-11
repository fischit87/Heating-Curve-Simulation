"""Sensors for Heating Curve Simulator."""
from __future__ import annotations

from decimal import Decimal, ROUND_HALF_UP

from homeassistant.components.sensor import SensorEntity
from homeassistant.const import UnitOfTemperature
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.event import async_track_state_change_event

from . import DOMAIN

OUTDOOR_TEMPERATURES = [-10, -5, 0, 5, 10, 15, 20]


async def async_setup_platform(
    hass: HomeAssistant,
    config: dict,
    async_add_entities: AddEntitiesCallback,
    discovery_info=None,
) -> None:
    """Set up Heating Curve Simulator sensors."""
    entities = [HeatingCurveFlowSensor(hass, outdoor_temp) for outdoor_temp in OUTDOOR_TEMPERATURES]
    async_add_entities(entities)


class HeatingCurveFlowSensor(SensorEntity):
    """Calculated target flow temperature sensor."""

    _attr_should_poll = False
    _attr_has_entity_name = True
    _tracked_entities = [
        f"input_number.{DOMAIN}_slope",
        f"input_number.{DOMAIN}_level",
        f"input_number.{DOMAIN}_room_setpoint",
    ]

    def __init__(self, hass: HomeAssistant, outdoor_temperature: int) -> None:
        self.hass = hass
        self._outdoor_temperature = outdoor_temperature
        self._attr_name = f"Soll Vorlauftemperatur bei {outdoor_temperature}°C Außentemperatur"
        self._attr_unique_id = f"{DOMAIN}_flow_temp_{outdoor_temperature}"
        self._attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
        self._attr_icon = "mdi:radiator"
        self.entity_id = f"sensor.{DOMAIN}_flow_temp_{self._sanitize(outdoor_temperature)}c"
        self._unsub_state_changed = None

    async def async_added_to_hass(self) -> None:
        """Register update listeners."""
        await super().async_added_to_hass()

        @callback
        def _handle_state_change(event):
            self.async_write_ha_state()

        self._unsub_state_changed = async_track_state_change_event(
            self.hass,
            self._tracked_entities,
            _handle_state_change,
        )

    async def async_will_remove_from_hass(self) -> None:
        """Clean up listeners."""
        if self._unsub_state_changed is not None:
            self._unsub_state_changed()

    @property
    def native_value(self) -> float | None:
        """Return the calculated target flow temperature."""
        slope = self._get_input_value(f"input_number.{DOMAIN}_slope")
        level = self._get_input_value(f"input_number.{DOMAIN}_level")
        room_setpoint = self._get_input_value(f"input_number.{DOMAIN}_room_setpoint")

        if slope is None or level is None or room_setpoint is None:
            return None

        dar = self._outdoor_temperature - room_setpoint
        result = room_setpoint + level - slope * dar * (
            1.4347 + 0.021 * dar + 247.9e-6 * dar * dar
        )
        return float(Decimal(str(result)).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP))

    @property
    def extra_state_attributes(self) -> dict:
        """Return extra attributes for traceability."""
        slope = self._get_input_value(f"input_number.{DOMAIN}_slope")
        level = self._get_input_value(f"input_number.{DOMAIN}_level")
        room_setpoint = self._get_input_value(f"input_number.{DOMAIN}_room_setpoint")
        dar = None if room_setpoint is None else self._outdoor_temperature - room_setpoint
        return {
            "outdoor_temperature": self._outdoor_temperature,
            "dar": dar,
            "slope": slope,
            "level": level,
            "room_setpoint": room_setpoint,
            "formula": "room_setpoint + level - slope * dar * (1.4347 + 0.021 * dar + 247.9e-6 * dar * dar)",
        }

    def _get_input_value(self, entity_id: str) -> float | None:
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
