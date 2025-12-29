"""Sensor platform for Listing Home Assistant integration."""
from __future__ import annotations

from datetime import datetime
import logging

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import ListingDataUpdateCoordinator
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        [
            ListingDevicesSensor(coordinator),
            ListingEntitiesSensor(coordinator),
            ListingAutomationsSensor(coordinator),
            ListingScriptsSensor(coordinator),
            ListingScenesSensor(coordinator),
            ListingInputsSensor(coordinator),
            ListingSummarySensor(coordinator),
        ]
    )


class ListingBaseSensor(CoordinatorEntity, SensorEntity):
    """Base class for listing sensors."""

    def __init__(self, coordinator: ListingDataUpdateCoordinator, sensor_type: str) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._sensor_type = sensor_type
        self._attr_has_entity_name = True
        self._attr_unique_id = f"{DOMAIN}_{sensor_type}"
        self._attr_icon = self._get_icon()

    def _get_icon(self) -> str:
        """Return the icon for the sensor."""
        icons = {
            "devices": "mdi:devices",
            "entities": "mdi:format-list-bulleted",
            "automations": "mdi:robot",
            "scripts": "mdi:script-text",
            "scenes": "mdi:palette",
            "inputs": "mdi:form-textbox",
            "summary": "mdi:file-document",
        }
        return icons.get(self._sensor_type, "mdi:information")

    @property
    def device_info(self):
        """Return device info."""
        return {
            "identifiers": {(DOMAIN, "listing_homeassistant")},
            "name": "Listing Home Assistant",
            "manufacturer": "Turiko313",
            "model": "Home Assistant Listing",
            "sw_version": "1.0.0",
        }
    
    def _get_last_update(self) -> str:
        """Return the last update timestamp."""
        return datetime.now().isoformat()


class ListingDevicesSensor(ListingBaseSensor):
    """Sensor for devices count."""

    def __init__(self, coordinator: ListingDataUpdateCoordinator) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, "devices")
        self._attr_name = "Devices"

    @property
    def native_value(self) -> int:
        """Return the state of the sensor."""
        if self.coordinator.data:
            return len(self.coordinator.data.get("devices", []))
        return 0

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        if not self.coordinator.data:
            return {}
        
        devices = self.coordinator.data.get("devices", [])
        return {
            "devices": devices,
            "count": len(devices),
            "last_update": self._get_last_update(),
        }


class ListingEntitiesSensor(ListingBaseSensor):
    """Sensor for entities count."""

    def __init__(self, coordinator: ListingDataUpdateCoordinator) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, "entities")
        self._attr_name = "Entities"

    @property
    def native_value(self) -> int:
        """Return the state of the sensor."""
        if self.coordinator.data:
            entities = self.coordinator.data.get("entities", {})
            return sum(len(v) for v in entities.values())
        return 0

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        if not self.coordinator.data:
            return {}
        
        entities = self.coordinator.data.get("entities", {})
        counts = {domain: len(ents) for domain, ents in entities.items()}
        
        return {
            "entities_by_domain": entities,
            "domain_counts": counts,
            "total_count": sum(counts.values()),
            "last_update": self._get_last_update(),
        }


class ListingAutomationsSensor(ListingBaseSensor):
    """Sensor for automations count."""

    def __init__(self, coordinator: ListingDataUpdateCoordinator) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, "automations")
        self._attr_name = "Automations"

    @property
    def native_value(self) -> int:
        """Return the state of the sensor."""
        if self.coordinator.data:
            return len(self.coordinator.data.get("automations", []))
        return 0

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        if not self.coordinator.data:
            return {}
        
        automations = self.coordinator.data.get("automations", [])
        return {
            "automations": automations,
            "count": len(automations),
            "last_update": self._get_last_update(),
        }


class ListingScriptsSensor(ListingBaseSensor):
    """Sensor for scripts count."""

    def __init__(self, coordinator: ListingDataUpdateCoordinator) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, "scripts")
        self._attr_name = "Scripts"

    @property
    def native_value(self) -> int:
        """Return the state of the sensor."""
        if self.coordinator.data:
            return len(self.coordinator.data.get("scripts", []))
        return 0

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        if not self.coordinator.data:
            return {}
        
        scripts = self.coordinator.data.get("scripts", [])
        return {
            "scripts": scripts,
            "count": len(scripts),
            "last_update": self._get_last_update(),
        }


class ListingScenesSensor(ListingBaseSensor):
    """Sensor for scenes count."""

    def __init__(self, coordinator: ListingDataUpdateCoordinator) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, "scenes")
        self._attr_name = "Scenes"

    @property
    def native_value(self) -> int:
        """Return the state of the sensor."""
        if self.coordinator.data:
            return len(self.coordinator.data.get("scenes", []))
        return 0

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        if not self.coordinator.data:
            return {}
        
        scenes = self.coordinator.data.get("scenes", [])
        return {
            "scenes": scenes,
            "count": len(scenes),
            "last_update": self._get_last_update(),
        }


class ListingInputsSensor(ListingBaseSensor):
    """Sensor for inputs count."""

    def __init__(self, coordinator: ListingDataUpdateCoordinator) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, "inputs")
        self._attr_name = "Inputs"

    @property
    def native_value(self) -> int:
        """Return the state of the sensor."""
        if self.coordinator.data:
            inputs = self.coordinator.data.get("inputs", {})
            return sum(len(v) for v in inputs.values())
        return 0

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        if not self.coordinator.data:
            return {}
        
        inputs = self.coordinator.data.get("inputs", {})
        counts = {input_type: len(items) for input_type, items in inputs.items()}
        
        return {
            "inputs_by_type": inputs,
            "type_counts": counts,
            "total_count": sum(counts.values()),
            "last_update": self._get_last_update(),
        }


class ListingSummarySensor(ListingBaseSensor):
    """Summary sensor for all listings."""

    def __init__(self, coordinator: ListingDataUpdateCoordinator) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, "summary")
        self._attr_name = "Summary"

    @property
    def native_value(self) -> str:
        """Return the state of the sensor."""
        return "Ready"

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        if not self.coordinator.data:
            return {}
        
        data = self.coordinator.data
        entities = data.get("entities", {})
        inputs = data.get("inputs", {})
        
        return {
            "total_devices": len(data.get("devices", [])),
            "total_entities": sum(len(v) for v in entities.values()),
            "total_automations": len(data.get("automations", [])),
            "total_scripts": len(data.get("scripts", [])),
            "total_scenes": len(data.get("scenes", [])),
            "total_inputs": sum(len(v) for v in inputs.values()),
            "entity_domains": list(entities.keys()),
            "input_types": list(inputs.keys()),
            "last_update": self._get_last_update(),
        }
