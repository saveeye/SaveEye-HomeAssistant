from __future__ import annotations

from collections.abc import Callable
import json
import logging
from typing import Any, Dict, cast

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_NAME, Platform
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.typing import ConfigType
from homeassistant.components import mqtt
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import (
    CONF_FRIENDLY_NAME,
    CONF_TOPIC,
    DATA_KEY_COORDINATOR,
    DATA_KEY_UNSUBSCRIBE,
    DEFAULT_TOPIC,
    DOMAIN,
)

PLATFORMS: list[Platform] = [Platform.SENSOR]
LOGGER: logging.Logger = logging.getLogger(__name__)


class SaveEyeCoordinator(DataUpdateCoordinator[Dict[str, Any]]):
    """Coordinator storing latest SaveEye telemetry."""

    def __init__(self, hass: HomeAssistant, name: str) -> None:
        super().__init__(hass, logger=LOGGER, name=name)
        self._devices: Dict[str, Dict[str, Any]] = {}

    @property
    def devices(self) -> Dict[str, Dict[str, Any]]:
        return self._devices

    @callback
    def handle_payload(self, payload: Dict[str, Any]) -> None:
        """Update internal state from an incoming telemetry payload."""
        device_serial_raw: Any = payload.get("saveeyeDeviceSerialNumber")
        device_serial: str = str(device_serial_raw) if device_serial_raw is not None else "unknown"
        self._devices[device_serial] = payload
        self.async_set_updated_data(self._devices)


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up via YAML (not used)."""
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up SaveEye from a config entry."""
    topic: str = entry.data.get(CONF_TOPIC, DEFAULT_TOPIC)

    coordinator = SaveEyeCoordinator(hass, "SaveEye MQTT")

    async def message_received(msg: mqtt.ReceiveMessage) -> None:
        raw_payload: bytes | str = msg.payload

        try:
            if isinstance(raw_payload, bytes):
                decoded: str = raw_payload.decode("utf-8")
            else:
                decoded = raw_payload

            loaded: Any = json.loads(decoded)
            payload: Dict[str, Any] = cast(Dict[str, Any], loaded)
        except (UnicodeDecodeError, json.JSONDecodeError):
            LOGGER.warning("SaveEye MQTT: Failed to parse JSON from topic %s", msg.topic)
            return

        coordinator.handle_payload(payload)

    unsubscribe: Callable[[], None] = await mqtt.async_subscribe(hass, topic, message_received)

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {
        DATA_KEY_COORDINATOR: coordinator,
        DATA_KEY_UNSUBSCRIBE: unsubscribe,
    }

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    if unload_ok and DOMAIN in hass.data and entry.entry_id in hass.data[DOMAIN]:
        stored = hass.data[DOMAIN].pop(entry.entry_id)
        unsubscribe: Callable[[], None] | None = stored.get(DATA_KEY_UNSUBSCRIBE)
        if unsubscribe is not None:
            unsubscribe()

    return unload_ok
