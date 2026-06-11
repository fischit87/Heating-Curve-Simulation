# Heating Curve Simulator for Home Assistant

Diese Custom Integration legt drei `input_number`-Entitäten und sieben berechnete Sensoren an.

## Angelegte Input-Entitäten
- `input_number.heating_curve_simulator_slope` → Neigung (0.0 bis 2.0, Schrittweite 0.1)
- `input_number.heating_curve_simulator_level` → Niveau (-10 bis 10, Schrittweite 1)
- `input_number.heating_curve_simulator_room_setpoint` → Raumtemperatur Soll (15 bis 30 °C, Schrittweite 1)

## Angelegte Sensoren
- `sensor.heating_curve_simulator_flow_temp_minus_10c`
- `sensor.heating_curve_simulator_flow_temp_minus_5c`
- `sensor.heating_curve_simulator_flow_temp_0c`
- `sensor.heating_curve_simulator_flow_temp_5c`
- `sensor.heating_curve_simulator_flow_temp_10c`
- `sensor.heating_curve_simulator_flow_temp_15c`
- `sensor.heating_curve_simulator_flow_temp_20c`

## Berechnungsformel
```jinja2
{{ RaumtemperaturSoll + niveau - neigung * dar * (1.4347 + 0.021 * dar + 247.9e-6 * dar * dar)) | round(1) }}
```

Dabei gilt:
- `dar = aussentemperatur - RaumtemperaturSoll`

## Installation
1. Ordner `custom_components/heating_curve_simulator` nach `<config>/custom_components/` kopieren.
2. In `configuration.yaml` ergänzen:

```yaml
input_number:
  - platform: heating_curve_simulator

sensor:
  - platform: heating_curve_simulator
```

3. Home Assistant neu starten.

## Hinweise
- Die Werte der drei Input-Entitäten werden wiederhergestellt.
- Die Sensoren aktualisieren sich automatisch bei jeder Änderung der Inputs.
- Die Sensoren liefern zusätzlich Attribute für `dar`, Außentemperatur und verwendete Parameter.
