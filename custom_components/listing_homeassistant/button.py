"""Button platform for Listing Home Assistant."""
from __future__ import annotations

import logging
from datetime import datetime

from homeassistant.components.button import ButtonEntity
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

    def __init__(self, coordinator, entry):
        """Initialize the button."""
        super().__init__(coordinator)
        self._entry = entry
        self._attr_name = "Actualiser les données"
        self._attr_unique_id = f"{entry.entry_id}_refresh"
        self._attr_icon = "mdi:refresh"
        self._attr_entity_category = None

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

    async def async_press(self) -> None:
        """Handle the button press."""
        _LOGGER.info("Manual refresh triggered via button")
        await self.coordinator.async_request_refresh()


class ListingExportButton(CoordinatorEntity, ButtonEntity):
    """Button to export data as YAML."""

    def __init__(self, coordinator, entry, hass):
        """Initialize the button."""
        super().__init__(coordinator)
        self._entry = entry
        self._hass = hass
        self._attr_name = "Exporter en YAML"
        self._attr_unique_id = f"{entry.entry_id}_export"
        self._attr_icon = "mdi:download"
        self._attr_entity_category = None

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

    async def async_press(self) -> None:
        """Handle the button press."""
        _LOGGER.info("Export triggered via button")
        
        # Create a persistent notification with download link
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        message = (
            f"Votre export YAML est prêt !\n\n"
            f"?? [Télécharger le fichier YAML](/api/listing_homeassistant/download)\n\n"
            f"Le fichier sera nommé: listing_homeassistant_{timestamp}.yaml"
        )
        
        self._hass.components.persistent_notification.async_create(
            message,
            title="?? Export YAML disponible",
            notification_id=f"listing_homeassistant_export_{timestamp}"
        )
