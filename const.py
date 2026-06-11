"""Constants for Heating Curve Simulator."""
from __future__ import annotations

DOMAIN = "heating_curve_simulator"
DEFAULT_NAME = "Heating Curve Simulator"
OUTDOOR_TEMPERATURES = [-10, -5, 0, 5, 10, 15, 20]

CONF_SLOPE = "slope"
CONF_LEVEL = "level"
CONF_ROOM_SETPOINT = "room_setpoint"

DEFAULT_SLOPE = 1.0
DEFAULT_LEVEL = 0.0
DEFAULT_ROOM_SETPOINT = 20.0
