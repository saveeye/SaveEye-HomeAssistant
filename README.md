## SaveEye – Home Assistant Custom Integration

**SaveEye** is a Home Assistant custom integration that exposes telemetry from SaveEye devices publishing over MQTT (for example on the `saveeye/telemetry` topic). It removes the need for manual YAML sensor definitions and is fully configurable from the Home Assistant UI.

### Features

- **UI-only configuration** via Home Assistant config flow (no YAML required).
- **MQTT-based**: subscribes to a configurable topic (default `saveeye/telemetry`).
- Creates sensor entities for key SaveEye metrics (energy, power, voltage, current, Wi‑Fi RSSI etc.).
- Designed to be installed as a **HACS custom repository**.

### Prerequisites

- A running Home Assistant instance.
- HACS setup and running
- MQTT broker configured in Home Assistant (e.g. Mosquitto add-on).
- SaveEye device configured for **Local MQTT** via the SaveEye app, pointing to the same broker and topic.

### Installation via HACS

- In Home Assistant, make sure HACS is installed.
- In HACS, add this repository as a **Custom repository** of type `Integration`.
- Install **SaveEye** from HACS.
- Restart Home Assistant.

### Configuration

- Go to **Settings → Devices & services → Add integration** and search for **SaveEye**.
- Enter:
  - **Device name** – a friendly label used for the device.
  - **MQTT topic** – keep the default `saveeye/telemetry` or adjust if you use another topic.
- Finish the flow; entities will start updating as soon as telemetry messages arrive on the topic.

### Notes

- This integration assumes a single SaveEye device publishing on the configured topic.
