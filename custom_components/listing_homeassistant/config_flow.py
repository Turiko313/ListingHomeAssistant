"""Config flow for Listing Home Assistant integration."""
from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.config_entries import ConfigFlow, ConfigFlowResult, OptionsFlow
from homeassistant.core import callback

from .const import DOMAIN, CONF_UPDATE_INTERVAL, UPDATE_INTERVALS


class ListingHomeAssistantConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Listing Home Assistant."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial step."""
        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")

        if user_input is not None:
            return self.async_create_entry(title="Listing Home Assistant", data={})

        return self.async_show_form(step_id="user", data_schema=vol.Schema({}))

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> OptionsFlow:
        """Get the options flow for this handler."""
        return ListingHomeAssistantOptionsFlow()


class ListingHomeAssistantOptionsFlow(OptionsFlow):
    """Handle options flow for Listing Home Assistant."""

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Manage the options."""
        if user_input is not None:
            # Merge with existing options to avoid overriding values set by other entities (e.g. Select export section)
            new_options = {**self.config_entry.options, **user_input}
            return self.async_create_entry(title="", data=new_options)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_UPDATE_INTERVAL,
                        default=self.config_entry.options.get(
                            CONF_UPDATE_INTERVAL, UPDATE_INTERVALS["1_hour"]
                        ),
                    ): vol.In(
                        {
                            UPDATE_INTERVALS["1_hour"]: "Every hour",
                            UPDATE_INTERVALS["6_hours"]: "Every 6 hours",
                            UPDATE_INTERVALS["12_hours"]: "Every 12 hours",
                            UPDATE_INTERVALS["1_day"]: "Every day",
                        }
                    )
                }
            ),
        )
