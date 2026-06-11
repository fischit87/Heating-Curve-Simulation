"""Base entity for Heating Curve Simulator."""
from __future__ import annotations

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity import Entity

from .const import DOMAIN


class HeatingCurveSimulatorEntity(Entity):
    """Base entity class."""

    _attr_has_entity_name = True

    def __init__(self, entry_id: str) -> None:
        self._entry_id = entry_id

    @property
    def device_info(self) -> DeviceInfo:
        """Return device info."""
        return DeviceInfo(
            identifiers={(DOMAIN, self._entry_id)},
            name="Heating Curve Simulator",
            manufacturer="Custom",
            model="Heating Curve Formula",
        )
