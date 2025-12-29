"""Download handler for Listing Home Assistant."""
from __future__ import annotations

import logging
from datetime import datetime

from aiohttp import web
import yaml

from homeassistant.components.http import HomeAssistantView
from homeassistant.core import HomeAssistant

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class ListingDownloadView(HomeAssistantView):
    """View to download the YAML export."""

    url = "/api/listing_homeassistant/download"
    name = "api:listing_homeassistant:download"
    requires_auth = True

    def __init__(self, hass: HomeAssistant) -> None:
        """Initialize the view."""
        self.hass = hass

    async def get(self, request):
        """Handle GET request."""
        # Get data from the first coordinator
        if not self.hass.data.get(DOMAIN):
            return web.Response(text="No data available", status=404)
        
        # Get the first coordinator (should only be one entry)
        coordinator = None
        for entry_id, coord in self.hass.data[DOMAIN].items():
            if entry_id != "yaml_export" and hasattr(coord, 'data'):
                coordinator = coord
                break
        
        if not coordinator or not coordinator.data:
            return web.Response(text="No data available", status=404)
        
        data = coordinator.data
        
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
                    key=lambda x: x.get("name", "") or ""
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
        
        # Create filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"listing_homeassistant_{timestamp}.yaml"
        
        # Return as downloadable file
        return web.Response(
            body=yaml_content.encode('utf-8'),
            headers={
                'Content-Type': 'application/x-yaml',
                'Content-Disposition': f'attachment; filename="{filename}"'
            }
        )


async def async_setup_download_handler(hass: HomeAssistant) -> None:
    """Set up the download handler."""
    hass.http.register_view(ListingDownloadView(hass))
