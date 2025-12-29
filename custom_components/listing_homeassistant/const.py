"""Constants for the Listing Home Assistant integration."""

DOMAIN = "listing_homeassistant"

CONF_UPDATE_INTERVAL = "update_interval"

# Update interval options (in seconds)
UPDATE_INTERVALS = {
    "1_hour": 3600,
    "6_hours": 21600,
    "12_hours": 43200,
    "1_day": 86400,
}

# Special key for YAML export data storage
YAML_EXPORT_KEY = "yaml_export"
