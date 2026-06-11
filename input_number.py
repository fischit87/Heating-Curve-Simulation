"""Input numbers for Heating Curve Simulator."""
from __future__ import annotations

from homeassistant.components.input_number import RestoreNumber
from homeassistant.components.number import NumberMode
from homeassistant.const import UnitOfTemperature
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.restore_state import RestoreEntity

from . import DOMAIN

INPUTS = [
    {
        "key": "slope",
        "name": "Neigung",
        "icon": "mdi:chart-line",
        "min": 0.0,
        "max": 2.0,
        "step": 0.1,
        "initial": 1.0,
        "unit": None,
    },
    {
        "key": "level",
        "name": "Niveau",
        "icon": "mdi:tune-vertical",
        "min": -10.0,
        "max": 10.0,
        "step": 1.0,
        "initial": 0.0,
        "unit": "K",
    },
    {
        "key": "room_setpoint",
        "name": "Raumtemperatur Soll",
        "icon": "mdi:home-thermometer-outline",
        "min": 15.0,
        "max": 30.0,
        "step": 1.0,
        "initial": 20.0,
        "unit": UnitOfTemperature.CELSIUS,
    },
]


async def async_setup_platform(
    hass: HomeAssistant,
    config: dict,
    async_add_entities: AddEntitiesCallback,
    discovery_info=None,
) -> None:
    """Set up Heating Curve Simulator input numbers."""
    entities = [HeatingCurveInputNumber(definition) for definition in INPUTS]
    async_add_entities(entities)


class HeatingCurveInputNumber(RestoreNumber, RestoreEntity):
    """Representation of an input number for the Heating Curve Simulator."""

    _attr_should_poll = False
    _attr_mode = NumberMode.SLIDER
    _attr_has_entity_name = True

    def __init__(self, definition: dict) -> None:
        self._definition = definition
        self._attr_name = definition["name"]
        self._attr_unique_id = f"{DOMAIN}_{definition['key']}"
        self._attr_icon = definition["icon"]
        self._attr_native_min_value = definition["min"]
        self._attr_native_max_value = definition["max"]
        self._attr_native_step = definition["step"]
        self._attr_native_unit_of_measurement = definition["unit"]
        self._attr_native_value = definition["initial"]
        self.entity_id = f"input_number.{DOMAIN}_{definition['key']}"

    async def async_added_to_hass(self) -> None:
        """Restore previous state."""
        await super().async_added_to_hass()
        last_number_data = await self.async_get_last_number_data()
        if last_number_data is not None:
            self._attr_native_value = last_number_data.native_value

    async def async_set_native_value(self, value: float) -> None:
        """Set the value of the number entity."""
        self._attr_native_value = value
        self.async_write_ha_state()
