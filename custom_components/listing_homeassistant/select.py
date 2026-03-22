"""Select platform for Listing Home Assistant."""
from __future__ import annotations

import logging

from homeassistant.components.select import SelectEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    DOMAIN,
    CONF_UPDATE_INTERVAL,
    UPDATE_INTERVALS,
    CONF_EXPORT_SECTION,
    EXPORT_SECTIONS,
)

_LOGGER = logging.getLogger(__name__)

# Internal keys mapped to interval values (seconds)
_KEY_TO_VALUE = {
    "every_hour": UPDATE_INTERVALS["1_hour"],
    "every_6_hours": UPDATE_INTERVALS["6_hours"],
    "every_12_hours": UPDATE_INTERVALS["12_hours"],
    "every_day": UPDATE_INTERVALS["1_day"],
}

_VALUE_TO_KEY = {v: k for k, v in _KEY_TO_VALUE.items()}


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Listing Home Assistant select entities."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([
        ListingUpdateIntervalSelect(coordinator, entry, hass),
        ListingExportSectionSelect(coordinator, entry, hass),
    ])


class ListingUpdateIntervalSelect(CoordinatorEntity, SelectEntity):
    """Select entity to configure update interval."""

    _attr_has_entity_name = True
    _attr_translation_key = "update_interval"

    def __init__(self, coordinator, entry, hass):
        """Initialize the select."""
        super().__init__(coordinator)
        self._entry = entry
        self._hass = hass
        self._attr_unique_id = f"{entry.entry_id}_update_interval"
        self._attr_icon = "mdi:timer-cog"
        self._attr_options = list(_KEY_TO_VALUE.keys())

    @property
    def device_info(self):
        """Return device info."""
        return {
            "identifiers": {(DOMAIN, "listing_homeassistant")},
            "name": "Listing Home Assistant",
            "manufacturer": "Turiko313",
            "model": "Home Assistant Listing",
        }

    @property
    def current_option(self) -> str:
        """Return the current selected option."""
        current_value = self._entry.options.get(
            CONF_UPDATE_INTERVAL, UPDATE_INTERVALS["1_hour"]
        )
        return _VALUE_TO_KEY.get(current_value, "every_hour")

    async def async_select_option(self, option: str) -> None:
        """Change the selected option."""
        new_value = _KEY_TO_VALUE.get(option)
        if new_value is not None:
            new_options = {**self._entry.options, CONF_UPDATE_INTERVAL: new_value}
            self._hass.config_entries.async_update_entry(
                self._entry, options=new_options
            )
            _LOGGER.info(
                "Update interval changed to %s (%s seconds)", option, new_value
            )


class ListingExportSectionSelect(CoordinatorEntity, SelectEntity):
    """Select entity to choose which section to export."""

    _attr_has_entity_name = True
    _attr_translation_key = "export_section"

    def __init__(self, coordinator, entry, hass):
        """Initialize the select."""
        super().__init__(coordinator)
        self._entry = entry
        self._hass = hass
        self._attr_unique_id = f"{entry.entry_id}_export_section"
        self._attr_icon = "mdi:filter-variant"
        self._attr_options = EXPORT_SECTIONS

    @property
    def device_info(self):
        """Return device info."""
        return {
            "identifiers": {(DOMAIN, "listing_homeassistant")},
            "name": "Listing Home Assistant",
            "manufacturer": "Turiko313",
            "model": "Home Assistant Listing",
        }

    @property
    def current_option(self) -> str:
        """Return the current selected option."""
        return self._entry.options.get(CONF_EXPORT_SECTION, "all")

    async def async_select_option(self, option: str) -> None:
        """Change the selected option."""
        if option in EXPORT_SECTIONS:
            new_options = {**self._entry.options, CONF_EXPORT_SECTION: option}
            self._hass.config_entries.async_update_entry(
                self._entry, options=new_options
            )
            _LOGGER.info("Export section changed to %s", option)