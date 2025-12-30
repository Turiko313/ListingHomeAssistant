"""Config flow for Listing Home Assistant integration."""
from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult

from .const import DOMAIN, CONF_UPDATE_INTERVAL, UPDATE_INTERVALS

_LOGGER = logging.getLogger(__name__)


class ListingHomeAssistantConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Listing Home Assistant."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")

        if user_input is not None:
            return self.async_create_entry(
                title="Listing Home Assistant",
                data={},
            )

        return self.async_show_form(step_id="user", data_schema=vol.Schema({}))

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> ListingHomeAssistantOptionsFlow:
        """Get the options flow for this handler."""
        return ListingHomeAssistantOptionsFlow(config_entry)


class ListingHomeAssistantOptionsFlow(config_entries.OptionsFlow):
    """Handle options flow for Listing Home Assistant."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        self._config_entry = config_entry

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Manage the options."""
        if user_input is not None:
            # Handle actions
            if user_input.get("action") == "refresh":
                await self.hass.services.async_call(DOMAIN, "refresh", {})
                return await self.async_step_init()
            elif user_input.get("action") == "export":
                # Trigger export notification
                self.hass.components.persistent_notification.async_create(
                    f"Téléchargez votre export ici:\n[Télécharger YAML](/api/listing_homeassistant/download)",
                    title="Export YAML disponible",
                    notification_id="listing_homeassistant_export",
                )
                return await self.async_step_init()
            else:
                # Save update interval
                return self.async_create_entry(title="", data=user_input)

        # Get statistics from coordinator
        coordinator = None
        for entry_id, coord in self.hass.data.get(DOMAIN, {}).items():
            if hasattr(coord, "data"):
                coordinator = coord
                break

        stats_text = "Statistiques:\n\n"
        if coordinator and coordinator.data:
            data = coordinator.data
            stats_text += f"?? Appareils: {len(data.get('devices', []))}\n"
            stats_text += f"?? Entités: {sum(len(v) for v in data.get('entities', {}).values())}\n"
            stats_text += f"?? Automatisations: {len(data.get('automations', []))}\n"
            stats_text += f"?? Scripts: {len(data.get('scripts', []))}\n"
            stats_text += f"?? Scènes: {len(data.get('scenes', []))}\n"
            stats_text += f"?? Inputs: {sum(len(v) for v in data.get('inputs', {}).values())}\n"
        else:
            stats_text += "Aucune donnée disponible. Cliquez sur 'Actualiser'.\n"

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Optional("action"): vol.In(
                        {
                            "refresh": "?? Actualiser les données",
                            "export": "?? Exporter en YAML",
                            "configure": "?? Configurer l'intervalle",
                        }
                    ),
                    vol.Optional(
                        CONF_UPDATE_INTERVAL,
                        default=self._config_entry.options.get(
                            CONF_UPDATE_INTERVAL, UPDATE_INTERVALS["1_hour"]
                        ),
                    ): vol.In(
                        {
                            UPDATE_INTERVALS["1_hour"]: "Toutes les heures",
                            UPDATE_INTERVALS["6_hours"]: "Toutes les 6 heures",
                            UPDATE_INTERVALS["12_hours"]: "Toutes les 12 heures",
                            UPDATE_INTERVALS["1_day"]: "Tous les jours",
                        }
                    ),
                }
            ),
            description_placeholders={"stats": stats_text},
        )
