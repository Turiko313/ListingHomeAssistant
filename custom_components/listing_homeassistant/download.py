"""Download handler for Listing Home Assistant."""
from __future__ import annotations

import logging
from datetime import datetime

from aiohttp import web
import yaml

from homeassistant.components.http import HomeAssistantView
from homeassistant.core import HomeAssistant

from .const import DOMAIN, YAML_EXPORT_KEY, EXPORT_SECTIONS

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

        coordinator = None
        for entry_id, coord in self.hass.data[DOMAIN].items():
            if entry_id != YAML_EXPORT_KEY and hasattr(coord, 'data'):
                coordinator = coord
                break

        if not coordinator or not coordinator.data:
            return web.Response(text="No data available", status=404)

        data = coordinator.data
        section = request.query.get("section", "all")
        if section not in EXPORT_SECTIONS:
            section = "all"

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        if section == "all":
            export_data = self._build_full_export(data)
            filename = f"listing_homeassistant_{timestamp}.yaml"
        else:
            export_data = self._build_section_export(data, section)
            filename = f"listing_{section}_{timestamp}.yaml"

        yaml_content = yaml.dump(
            export_data,
            allow_unicode=True,
            default_flow_style=False,
            sort_keys=False,
        )

        return web.Response(
            body=yaml_content.encode('utf-8'),
            headers={
                'Content-Type': 'application/x-yaml',
                'Content-Disposition': f'attachment; filename="{filename}"'
            }
        )

    @staticmethod
    def _build_full_export(data):
        """Build the full export with all sections."""
        return {
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
                    key=lambda x: x.get("name", "") or ""
                ),
                "entities": {
                    domain: sorted(entities, key=lambda x: x.get("entity_id", ""))
                    for domain, entities in sorted(
                        data.get("entities", {}).items()
                    )
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
                    input_type: sorted(
                        items, key=lambda x: x.get("entity_id", "")
                    )
                    for input_type, items in sorted(
                        data.get("inputs", {}).items()
                    )
                },
                "blueprints": data.get("blueprints", {}),
            }
        }

    @staticmethod
    def _build_section_export(data, section):
        """Build an export for a single section."""
        export = {
            "listing_home_assistant": {
                "export_date": datetime.now().isoformat(),
                "section": section,
            }
        }
        content = export["listing_home_assistant"]

        if section == "devices":
            items = sorted(
                data.get("devices", []),
                key=lambda x: x.get("name", "") or ""
            )
            content["total"] = len(items)
            content["devices"] = items

        elif section == "entities":
            entities = {
                domain: sorted(ents, key=lambda x: x.get("entity_id", ""))
                for domain, ents in sorted(
                    data.get("entities", {}).items()
                )
            }
            content["total"] = sum(len(v) for v in entities.values())
            content["entities"] = entities

        elif section == "automations":
            items = sorted(
                data.get("automations", []),
                key=lambda x: x.get("entity_id", "")
            )
            content["total"] = len(items)
            content["automations"] = items

        elif section == "scripts":
            items = sorted(
                data.get("scripts", []),
                key=lambda x: x.get("entity_id", "")
            )
            content["total"] = len(items)
            content["scripts"] = items

        elif section == "scenes":
            items = sorted(
                data.get("scenes", []),
                key=lambda x: x.get("entity_id", "")
            )
            content["total"] = len(items)
            content["scenes"] = items

        elif section == "inputs":
            inputs = {
                input_type: sorted(
                    items, key=lambda x: x.get("entity_id", "")
                )
                for input_type, items in sorted(
                    data.get("inputs", {}).items()
                )
            }
            content["total"] = sum(len(v) for v in inputs.values())
            content["inputs"] = inputs

        elif section == "blueprints":
            content["blueprints"] = data.get("blueprints", {})

        return export


async def async_setup_download_handler(hass: HomeAssistant) -> None:
    """Set up the download handler."""
    hass.http.register_view(ListingDownloadView(hass))
