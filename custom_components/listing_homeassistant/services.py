"""Services for Listing Home Assistant integration."""
from __future__ import annotations

import logging

from homeassistant.core import HomeAssistant, ServiceCall
import voluptuous as vol

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

SERVICE_REFRESH = "refresh"

SERVICE_REFRESH_SCHEMA = vol.Schema({})


async def async_setup_services(hass: HomeAssistant) -> None:
    """Set up services for Listing Home Assistant integration."""

    async def handle_refresh(call: ServiceCall) -> None:
        """Handle the refresh service call."""
        _LOGGER.info("Refreshing Listing Home Assistant data")
        
        # Refresh all coordinators
        for entry_id, coordinator in hass.data[DOMAIN].items():
            if hasattr(coordinator, 'async_refresh'):
                await coordinator.async_refresh()

    hass.services.async_register(
        DOMAIN,
        SERVICE_REFRESH,
        handle_refresh,
        schema=SERVICE_REFRESH_SCHEMA,
    )


async def async_unload_services(hass: HomeAssistant) -> None:
    """Unload Listing Home Assistant services."""
    hass.services.async_remove(DOMAIN, SERVICE_REFRESH)
