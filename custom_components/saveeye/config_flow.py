from __future__ import annotations

from typing import Any, Dict

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_NAME
from homeassistant.core import HomeAssistant

from .const import CONF_FRIENDLY_NAME, DOMAIN, CONF_SERIAL_NUMBER


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
            serial_number: str = user_input.get(CONF_SERIAL_NUMBER, "").strip()
            friendly_name: str = user_input.get(CONF_FRIENDLY_NAME, "SaveEye")

            if not serial_number:
                errors["base"] = "invalid_serial_number"
            else:
                await self.async_set_unique_id(serial_number)
                self._abort_if_unique_id_configured()

                data: Dict[str, Any] = {
                    CONF_SERIAL_NUMBER: serial_number,
                    CONF_FRIENDLY_NAME: friendly_name,
                    CONF_NAME: friendly_name,
                }
                return self.async_create_entry(title=f"{friendly_name} ({serial_number})", data=data)

        data_schema = vol.Schema(
            {
                vol.Required(CONF_SERIAL_NUMBER): str,
                vol.Optional(CONF_FRIENDLY_NAME, default="SaveEye"): str,
            }
        )

        return self.async_show_form(step_id="user", data_schema=data_schema, errors=errors)
