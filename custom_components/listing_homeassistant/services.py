"""Services for Listing Home Assistant integration."""
from __future__ import annotations

import logging
import yaml
from datetime import datetime

from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers import config_validation as cv
import voluptuous as vol

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

SERVICE_REFRESH = "refresh"
SERVICE_EXPORT_YAML = "export_yaml"

SERVICE_REFRESH_SCHEMA = vol.Schema({})
SERVICE_EXPORT_YAML_SCHEMA = vol.Schema({})


async def async_setup_services(hass: HomeAssistant) -> None:
    """Set up services for Listing Home Assistant integration."""

    async def handle_refresh(call: ServiceCall) -> None:
        """Handle the refresh service call."""
        _LOGGER.info("Refreshing Listing Home Assistant data")
        
        # Refresh all coordinators
        for entry_id, coordinator in hass.data[DOMAIN].items():
            await coordinator.async_refresh()

    async def handle_export_yaml(call: ServiceCall) -> None:
        """Handle the export YAML service call."""
        _LOGGER.info("Exporting Listing Home Assistant data to YAML")
        
        # Get data from the first coordinator (should only be one entry)
        if not hass.data.get(DOMAIN):
            _LOGGER.error("No Listing Home Assistant data available")
            return
        
        # Get the first coordinator
        coordinator = list(hass.data[DOMAIN].values())[0]
        data = coordinator.data
        
        if not data:
            _LOGGER.error("No data available to export")
            return
        
        # Prepare YAML structure
        export_data = {
            "listing_home_assistant": {
                "export_date": datetime.now().isoformat(),
                "summary": {
                    "total_devices": len(data.get("devices", [])),
                    "total_entities": sum(len(v) for v in data.get("entities", {}).values()),
                    "total_automations": len(data.get("automations", [])),
                    "total_scripts": len(data.get("scripts", [])),
                    "total_scenes": len(data.get("scenes", [])),
                    "total_inputs": sum(len(v) for v in data.get("inputs", {}).values()),
                },
                "devices": sorted(
                    data.get("devices", []),
                    key=lambda x: x.get("name", "")
                ),
                "entities": {
                    domain: sorted(entities, key=lambda x: x.get("entity_id", ""))
                    for domain, entities in sorted(data.get("entities", {}).items())
                },
                "automations": sorted(
                    data.get("automations", []),
                    key=lambda x: x.get("entity_id", "")
                ),
                "scripts": sorted(
                    data.get("scripts", []),
                    key=lambda x: x.get("entity_id", "")
                ),
                "scenes": sorted(
                    data.get("scenes", []),
                    key=lambda x: x.get("entity_id", "")
                ),
                "inputs": {
                    input_type: sorted(items, key=lambda x: x.get("entity_id", ""))
                    for input_type, items in sorted(data.get("inputs", {}).items())
                },
                "blueprints": data.get("blueprints", {}),
            }
        }
        
        # Convert to YAML
        yaml_content = yaml.dump(
            export_data,
            allow_unicode=True,
            default_flow_style=False,
            sort_keys=False,
        )
        
        # Store the YAML content in hass.data for the frontend to access
        if "yaml_export" not in hass.data[DOMAIN]:
            hass.data[DOMAIN]["yaml_export"] = {}
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"listing_homeassistant_{timestamp}.yaml"
        hass.data[DOMAIN]["yaml_export"]["content"] = yaml_content
        hass.data[DOMAIN]["yaml_export"]["filename"] = filename
        hass.data[DOMAIN]["yaml_export"]["timestamp"] = timestamp
        
        _LOGGER.info(f"YAML export ready: {filename}")
        
        # Fire an event that the frontend can listen to
        hass.bus.async_fire(
            f"{DOMAIN}_yaml_export_ready",
            {
                "filename": filename,
                "timestamp": timestamp,
                "size": len(yaml_content),
            }
        )

    hass.services.async_register(
        DOMAIN,
        SERVICE_REFRESH,
        handle_refresh,
        schema=SERVICE_REFRESH_SCHEMA,
    )

    hass.services.async_register(
        DOMAIN,
        SERVICE_EXPORT_YAML,
        handle_export_yaml,
        schema=SERVICE_EXPORT_YAML_SCHEMA,
    )


async def async_unload_services(hass: HomeAssistant) -> None:
    """Unload Listing Home Assistant services."""
    hass.services.async_remove(DOMAIN, SERVICE_REFRESH)
    hass.services.async_remove(DOMAIN, SERVICE_EXPORT_YAML)
