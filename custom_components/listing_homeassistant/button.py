"""Button platform for Listing Home Assistant."""
from __future__ import annotations

import logging
import os
from datetime import datetime

import yaml

from homeassistant.components.button import ButtonEntity
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

        if not self.coordinator.data:
            _LOGGER.warning("No data available for export")
            return

        data = self.coordinator.data

        # Build export structure
        export_data = {
            "listing_home_assistant": {
                "export_date": datetime.now().isoformat(),
                "summary": {
                    "total_devices": len(data.get("devices", [])),
                    "total_entities": sum(
                        len(v) for v in data.get("entities", {}).values()
                    ),
                    "total_automations": len(data.get("automations", [])),
                    "total_scripts": len(data.get("scripts", [])),
                    "total_scenes": len(data.get("scenes", [])),
                    "total_inputs": sum(
                        len(v) for v in data.get("inputs", {}).values()
                    ),
                },
                "devices": sorted(
                    data.get("devices", []),
                    key=lambda x: x.get("name", "") or "",
                ),
                "entities": {
                    domain: sorted(ents, key=lambda x: x.get("entity_id", ""))
                    for domain, ents in sorted(data.get("entities", {}).items())
                },
                "automations": sorted(
                    data.get("automations", []),
                    key=lambda x: x.get("entity_id", ""),
                ),
                "scripts": sorted(
                    data.get("scripts", []),
                    key=lambda x: x.get("entity_id", ""),
                ),
                "scenes": sorted(
                    data.get("scenes", []),
                    key=lambda x: x.get("entity_id", ""),
                ),
                "inputs": {
                    itype: sorted(items, key=lambda x: x.get("entity_id", ""))
                    for itype, items in sorted(data.get("inputs", {}).items())
                },
                "blueprints": data.get("blueprints", {}),
            }
        }

        yaml_content = yaml.dump(
            export_data,
            allow_unicode=True,
            default_flow_style=False,
            sort_keys=False,
        )

        # Save to www directory so HA serves it at /local/
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"listing_homeassistant_{timestamp}.yaml"
        export_dir = self._hass.config.path("www", "listing_homeassistant")
        filepath = os.path.join(export_dir, filename)

        def _write_export():
            os.makedirs(export_dir, exist_ok=True)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(yaml_content)

        await self._hass.async_add_executor_job(_write_export)

        _LOGGER.info("YAML export saved to %s", filepath)

        pn_create(
            self._hass,
            f"YAML export is ready!\n\n"
            f"[Download YAML file](/local/listing_homeassistant/{filename})\n\n"
            f"File: /config/www/listing_homeassistant/{filename}",
            title="YAML Export",
            notification_id=f"listing_homeassistant_export_{timestamp}",
        )
