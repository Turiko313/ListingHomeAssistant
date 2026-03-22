"""Button platform for Listing Home Assistant."""
from __future__ import annotations

import logging
from datetime import datetime, timedelta

from homeassistant.components.button import ButtonEntity
from homeassistant.components.http import async_sign_path
from homeassistant.components.persistent_notification import async_create as pn_create
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Listing Home Assistant button entities."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    
    entities = [
        ListingRefreshButton(coordinator, entry),
        ListingExportButton(coordinator, entry, hass),
    ]
    
    async_add_entities(entities)


class ListingRefreshButton(CoordinatorEntity, ButtonEntity):
    """Button to manually refresh listing data."""

    _attr_has_entity_name = True
    _attr_translation_key = "refresh"

    def __init__(self, coordinator, entry):
        """Initialize the button."""
        super().__init__(coordinator)
        self._entry = entry
        self._attr_unique_id = f"{entry.entry_id}_refresh"
        self._attr_icon = "mdi:refresh"

    @property
    def device_info(self):
        """Return device info."""
        return {
            "identifiers": {(DOMAIN, "listing_homeassistant")},
            "name": "Listing Home Assistant",
            "manufacturer": "Turiko313",
            "model": "Home Assistant Listing",
        }

    async def async_press(self) -> None:
        """Handle the button press."""
        _LOGGER.info("Manual refresh triggered via button")
        await self.coordinator.async_request_refresh()


class ListingExportButton(CoordinatorEntity, ButtonEntity):
    """Button to export data as YAML."""

    _attr_has_entity_name = True
    _attr_translation_key = "export_yaml"

    def __init__(self, coordinator, entry, hass):
        """Initialize the button."""
        super().__init__(coordinator)
        self._entry = entry
        self._hass = hass
        self._attr_unique_id = f"{entry.entry_id}_export"
        self._attr_icon = "mdi:download"

    @property
    def device_info(self):
        """Return device info."""
        return {
            "identifiers": {(DOMAIN, "listing_homeassistant")},
            "name": "Listing Home Assistant",
            "manufacturer": "Turiko313",
            "model": "Home Assistant Listing",
        }

    async def async_press(self) -> None:
        """Handle the button press."""
        _LOGGER.info("Export triggered via button")

        # Create a signed URL for the download endpoint (valid 30 min)
        signed_path = async_sign_path(
            self._hass,
            "/api/listing_homeassistant/download",
            timedelta(minutes=30),
        )

        pn_create(
            self._hass,
            "YAML export is ready!\n\n"
            f"[Download YAML file]({signed_path})\n\n"
            "Link valid for 30 minutes.",
            title="YAML Export",
            notification_id="listing_homeassistant_export",
        )
