from __future__ import annotations

from typing import Any, Dict

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_NAME
from homeassistant.core import HomeAssistant

from .const import CONF_FRIENDLY_NAME, CONF_TOPIC, DEFAULT_TOPIC, DOMAIN


async def _mqtt_available(hass: HomeAssistant) -> bool:
    """Return True if MQTT integration is loaded."""
    return "mqtt" in hass.config.components


class SaveEyeMqttConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for SaveEye MQTT."""

    VERSION = 1

    async def async_step_user(self, user_input: Dict[str, Any] | None = None):
        errors: Dict[str, str] = {}

        if not await _mqtt_available(self.hass):
            return self.async_abort(reason="mqtt_not_configured")

        if user_input is not None:
            topic: str = user_input.get(CONF_TOPIC, DEFAULT_TOPIC).strip()
            friendly_name: str = user_input.get(CONF_FRIENDLY_NAME, "SaveEye")

            if not topic:
                errors["base"] = "invalid_topic"
            else:
                data: Dict[str, Any] = {
                    CONF_TOPIC: topic,
                    CONF_FRIENDLY_NAME: friendly_name,
                    CONF_NAME: friendly_name,
                }
                return self.async_create_entry(title=friendly_name, data=data)

        data_schema = vol.Schema(
            {
                vol.Optional(CONF_FRIENDLY_NAME, default="SaveEye"): str,
                vol.Optional(CONF_TOPIC, default=DEFAULT_TOPIC): str,
            }
        )

        return self.async_show_form(step_id="user", data_schema=data_schema, errors=errors)
