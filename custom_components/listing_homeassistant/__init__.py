"""The Listing Home Assistant integration."""
from __future__ import annotations

import logging
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import DOMAIN, CONF_UPDATE_INTERVAL
from .services import async_setup_services, async_unload_services
from .download import async_setup_download_handler

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [Platform.SENSOR, Platform.BUTTON, Platform.SELECT]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Listing Home Assistant from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    
    # Get update interval from options, default to 3600 seconds (1 hour)
    update_interval = entry.options.get(CONF_UPDATE_INTERVAL, 3600)
    
    coordinator = ListingDataUpdateCoordinator(
        hass,
        _LOGGER,
        update_interval=timedelta(seconds=update_interval),
    )
    
    await coordinator.async_config_entry_first_refresh()
    
    hass.data[DOMAIN][entry.entry_id] = coordinator
    
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    
    # Register services only once (check if already registered)
    if not hass.services.has_service(DOMAIN, "refresh"):
        await async_setup_services(hass)
    
    # Register download handler only once
    if not hasattr(hass.http, f"_listing_homeassistant_download_registered"):
        await async_setup_download_handler(hass)
        setattr(hass.http, f"_listing_homeassistant_download_registered", True)
    
    # Register update listener
    entry.async_on_unload(entry.add_update_listener(update_listener))
    
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)
        
        # Only unload services if this is the last entry
        if not hass.data[DOMAIN]:
            await async_unload_services(hass)
            if hasattr(hass.http, f"_listing_homeassistant_download_registered"):
                delattr(hass.http, f"_listing_homeassistant_download_registered")
    
    return unload_ok


async def update_listener(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Handle options update."""
    await hass.config_entries.async_reload(entry.entry_id)


class ListingDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching listing data."""

    def __init__(
        self,
        hass: HomeAssistant,
        logger: logging.Logger,
        update_interval: timedelta,
    ) -> None:
        """Initialize."""
        super().__init__(
            hass,
            logger,
            name=DOMAIN,
            update_interval=update_interval,
        )

    async def _async_update_data(self):
        """Update data via library."""
        data = {
            "devices": [],
            "entities": {},
            "automations": [],
            "scripts": [],
            "scenes": [],
            "inputs": {},
            "blueprints": {},
        }

        # Get all entities
        from homeassistant.helpers import entity_registry, device_registry

        entities_registry = entity_registry.async_get(self.hass)
        devices_registry = device_registry.async_get(self.hass)

        # Get devices
        for device in devices_registry.devices.values():
            data["devices"].append({
                "id": device.id,
                "name": device.name_by_user or device.name,
                "manufacturer": device.manufacturer,
                "model": device.model,
                "sw_version": device.sw_version,
                "area_id": device.area_id,
            })

        # Get entities by domain
        for entity in entities_registry.entities.values():
            domain = entity.domain
            if domain not in data["entities"]:
                data["entities"][domain] = []

            state = self.hass.states.get(entity.entity_id)
            entity_data = {
                "entity_id": entity.entity_id,
                "name": entity.name or entity.original_name or entity.entity_id,
                "device_id": entity.device_id,
                "platform": entity.platform,
                "state": state.state if state else "unavailable",
                "attributes": dict(state.attributes) if state and state.attributes else {},
            }
            data["entities"][domain].append(entity_data)

        # Load full automation configs from storage
        automation_configs = await self._async_load_automation_configs()
        # Load full script configs from storage
        script_configs = await self._async_load_script_configs()

        # Get automations, scripts, scenes, and inputs
        for state in self.hass.states.async_all():
            entity_id = state.entity_id
            if entity_id.startswith("automation."):
                auto_id = state.attributes.get("id", "")
                auto_data = {
                    "entity_id": entity_id,
                    "name": state.attributes.get("friendly_name", entity_id),
                    "state": state.state,
                    "mode": state.attributes.get("current", "single"),
                    "last_triggered": str(state.attributes.get("last_triggered", "")),
                }
                # Enrich with full config if available
                if auto_id and auto_id in automation_configs:
                    cfg = automation_configs[auto_id]
                    auto_data["description"] = cfg.get("description", "")
                    auto_data["mode"] = cfg.get("mode", "single")
                    auto_data["triggers"] = cfg.get(
                        "triggers", cfg.get("trigger", [])
                    )
                    auto_data["conditions"] = cfg.get(
                        "conditions", cfg.get("condition", [])
                    )
                    auto_data["actions"] = cfg.get(
                        "actions", cfg.get("action", [])
                    )
                data["automations"].append(auto_data)
            elif entity_id.startswith("script."):
                script_obj_id = entity_id.split(".", 1)[1]
                script_data = {
                    "entity_id": entity_id,
                    "name": state.attributes.get("friendly_name", entity_id),
                    "state": state.state,
                }
                # Enrich with full config if available
                if script_obj_id in script_configs:
                    cfg = script_configs[script_obj_id]
                    script_data["description"] = cfg.get("description", "")
                    script_data["mode"] = cfg.get("mode", "single")
                    script_data["fields"] = cfg.get("fields", {})
                    script_data["sequence"] = cfg.get("sequence", [])
                data["scripts"].append(script_data)
            elif entity_id.startswith("scene."):
                data["scenes"].append({
                    "entity_id": entity_id,
                    "name": state.attributes.get("friendly_name", entity_id),
                })
            elif entity_id.startswith("input_"):
                input_type = entity_id.split(".")[0]
                if input_type not in data["inputs"]:
                    data["inputs"][input_type] = []
                data["inputs"][input_type].append({
                    "entity_id": entity_id,
                    "name": state.attributes.get("friendly_name", entity_id),
                    "state": state.state,
                })

        return data

    async def _async_load_automation_configs(self) -> dict:
        """Load full automation configs from HA storage."""
        def _read():
            import json
            configs = {}
            path = self.hass.config.path(".storage", "automations")
            try:
                with open(path, "r", encoding="utf-8") as fh:
                    store = json.load(fh)
                for item in store.get("data", {}).get("items", []):
                    if aid := item.get("id"):
                        configs[aid] = item
            except (FileNotFoundError, ValueError, KeyError):
                pass
            return configs
        return await self.hass.async_add_executor_job(_read)

    async def _async_load_script_configs(self) -> dict:
        """Load full script configs from HA storage."""
        def _read():
            import json
            configs = {}
            path = self.hass.config.path(".storage", "scripts")
            try:
                with open(path, "r", encoding="utf-8") as fh:
                    store = json.load(fh)
                for item in store.get("data", {}).get("items", []):
                    if sid := item.get("id"):
                        configs[sid] = item
            except (FileNotFoundError, ValueError, KeyError):
                pass
            return configs
        return await self.hass.async_add_executor_job(_read)
