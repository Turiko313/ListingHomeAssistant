"""Frontend panel for Listing Home Assistant."""
from homeassistant.components.frontend import add_extra_js_url
from homeassistant.core import HomeAssistant


async def async_register_panel(hass: HomeAssistant) -> None:
    """Register the frontend panel."""
    # Register the panel card
    hass.http.register_static_path(
        "/listing_homeassistant",
        hass.config.path("custom_components/listing_homeassistant/www"),
        cache_headers=False,
    )
