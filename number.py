"""Number entities for Heating Curve Simulator."""
from __future__ import annotations

from homeassistant.components.number import NumberEntity, NumberMode, RestoreNumber
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import (
    CONF_LEVEL,
    CONF_ROOM_SETPOINT,
    CONF_SLOPE,
    DEFAULT_LEVEL,
    DEFAULT_ROOM_SETPOINT,
    DEFAULT_SLOPE,
    DOMAIN,
)
from .entity import HeatingCurveSimulatorEntity

ENTITY_DEFINITIONS = [
    {
        "key": CONF_SLOPE,
        "translation_key": CONF_SLOPE,
        "name": "Neigung",
        "icon": "mdi:chart-line",
        "min": 0.0,
        "max": 2.0,
        "step": 0.1,
        "default": DEFAULT_SLOPE,
        "unit": None,
    },
    {
        "key": CONF_LEVEL,
        "translation_key": CONF_LEVEL,
        "name": "Niveau",
        "icon": "mdi:tune-vertical",
        "min": -10.0,
        "max": 10.0,
        "step": 1.0,
        "default": DEFAULT_LEVEL,
        "unit": "K",
    },
    {
        "key": CONF_ROOM_SETPOINT,
        "translation_key": CONF_ROOM_SETPOINT,
        "name": "Raumtemperatur Soll",
        "icon": "mdi:home-thermometer-outline",
        "min": 15.0,
        "max": 30.0,
        "step": 1.0,
        "default": DEFAULT_ROOM_SETPOINT,
        "unit": UnitOfTemperature.CELSIUS,
    },
]


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up number entities."""
    async_add_entities(
        HeatingCurveNumber(entry.entry_id, definition) for definition in ENTITY_DEFINITIONS
    )


class HeatingCurveNumber(HeatingCurveSimulatorEntity, RestoreNumber, NumberEntity):
    """Numeric input entity for heating curve settings."""

    _attr_mode = NumberMode.SLIDER
    _attr_should_poll = False

    def __init__(self, entry_id: str, definition: dict) -> None:
        super().__init__(entry_id)
        self._definition = definition
        self._attr_name = definition["name"]
        self._attr_unique_id = f"{entry_id}_{definition['key']}"
        self._attr_native_min_value = definition["min"]
        self._attr_native_max_value = definition["max"]
        self._attr_native_step = definition["step"]
        self._attr_native_unit_of_measurement = definition["unit"]
        self._attr_icon = definition["icon"]
        self._attr_native_value = definition["default"]

    async def async_added_to_hass(self) -> None:
        """Restore previous value."""
        await super().async_added_to_hass()
        last_number_data = await self.async_get_last_number_data()
        if last_number_data is not None:
            self._attr_native_value = last_number_data.native_value

    async def async_set_native_value(self, value: float) -> None:
        """Update the value."""
        self._attr_native_value = value
        self.async_write_ha_state()
