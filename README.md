<h2>I am not a developer, so this is just for fun and for anyone who might have use of it. </h2>
<p>Anyone who would like to support, please contact me.</p>

# Heating Curve Simulator

Diese Version ist als Home-Assistant-Custom-Integration aufgebaut und benötigt **keine** Einträge in der `configuration.yaml`.

## Funktionen
- 3 automatisch erzeugte `number`-Entitäten
- 7 automatisch erzeugte `sensor`-Entitäten
- Einrichtung über **Settings → Devices & Services → Add Integration**
- Werte der Number-Entitäten werden wiederhergestellt

## Angelegte Number-Entitäten
- `number.heating_curve_simulator_neigung`
- `number.heating_curve_simulator_niveau`
- `number.heating_curve_simulator_raumtemperatur_soll`

## Angelegte Sensoren
- Soll Vorlauftemperatur bei -10°C Außentemperatur
- Soll Vorlauftemperatur bei -5°C Außentemperatur
- Soll Vorlauftemperatur bei 0°C Außentemperatur
- Soll Vorlauftemperatur bei 5°C Außentemperatur
- Soll Vorlauftemperatur bei 10°C Außentemperatur
- Soll Vorlauftemperatur bei 15°C Außentemperatur
- Soll Vorlauftemperatur bei 20°C Außentemperatur

## Installation
1. Ordner `custom_components/heating_curve_simulator` nach `<config>/custom_components/` kopieren.
2. Home Assistant neu starten.
3. Unter **Einstellungen → Geräte & Dienste → Integration hinzufügen** nach `Heating Curve Simulator` suchen.
4. Integration hinzufügen.

## Formel
```jinja2
{{ RaumtemperaturSoll + niveau - neigung * dar * (1.4347 + 0.021 * dar + 247.9e-6 * dar * dar)) | round(1) }}
```

`dar = aussentemperatur - RaumtemperaturSoll`
