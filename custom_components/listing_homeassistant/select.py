"""Select platform for Listing Home Assistant."""
from __future__ import annotations

import logging
from datetime import timedelta

from homeassistant.components.select import SelectEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, CONF_UPDATE_INTERVAL, UPDATE_INTERVALS

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Listing Home Assistant select entities."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    
    entities = [
        ListingUpdateIntervalSelect(coordinator, entry, hass),
    ]
    
    async_add_entities(entities)


class ListingUpdateIntervalSelect(CoordinatorEntity, SelectEntity):
    """Select entity to configure update interval."""

    _attr_translation_key = "update_interval"

    def __init__(self, coordinator, entry, hass):
        """Initialize the select."""
        super().__init__(coordinator)
        self._entry = entry
        self._hass = hass
        self._attr_name = "Intervalle de mise à jour"
        self._attr_unique_id = f"{entry.entry_id}_update_interval"
        self._attr_icon = "mdi:timer-cog"
        self._attr_entity_category = None
        
        # Options for the select
        self._attr_options = [
            "Toutes les heures",
            "Toutes les 6 heures",
            "Toutes les 12 heures",
            "Tous les jours",
        ]
        
        # Mapping between labels and values
        self._label_to_value = {
            "Toutes les heures": UPDATE_INTERVALS["1_hour"],
            "Toutes les 6 heures": UPDATE_INTERVALS["6_hours"],
            "Toutes les 12 heures": UPDATE_INTERVALS["12_hours"],
            "Tous les jours": UPDATE_INTERVALS["1_day"],
        }
        
        self._value_to_label = {v: k for k, v in self._label_to_value.items()}

    @property
    def device_info(self):
        """Return device info."""
        return {
            "identifiers": {(DOMAIN, self._entry.entry_id)},
            "name": "Listing Home Assistant",
            "manufacturer": "Listing Home Assistant",
            "model": "Data Listing",
            "sw_version": "1.0.0",
        }

    @property
    def current_option(self) -> str:
        """Return the current selected option."""
        current_value = self._entry.options.get(CONF_UPDATE_INTERVAL, UPDATE_INTERVALS["1_hour"])
        return self._value_to_label.get(current_value, "Toutes les heures")

    async def async_select_option(self, option: str) -> None:
        """Change the selected option."""
        new_value = self._label_to_value.get(option)
        
        if new_value is not None:
            # Update the config entry options
            new_options = {**self._entry.options, CONF_UPDATE_INTERVAL: new_value}
            self._hass.config_entries.async_update_entry(
                self._entry, options=new_options
            )
            
            # Update coordinator interval
            self.coordinator.update_interval = timedelta(seconds=new_value)
            
            _LOGGER.info(f"Update interval changed to: {option} ({new_value} seconds)")
            
            # Request an immediate refresh with new interval
            await self.coordinator.async_request_refresh()
