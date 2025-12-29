# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-12-29

### Added

- Initial release of Listing Home Assistant integration
- Support for listing all Home Assistant devices
- Support for listing all entities grouped by domain
- Support for listing automations with last triggered time
- Support for listing scripts
- Support for listing scenes
- Support for listing input entities (input_boolean, input_number, etc.)
- Dedicated sensors for each type of data:
  - `sensor.listing_home_assistant_devices`
  - `sensor.listing_home_assistant_entities`
  - `sensor.listing_home_assistant_automations`
  - `sensor.listing_home_assistant_scripts`
  - `sensor.listing_home_assistant_scenes`
  - `sensor.listing_home_assistant_inputs`
  - `sensor.listing_home_assistant_summary`
- Manual refresh service: `listing_homeassistant.refresh`
- Configurable automatic refresh interval:
  - Every hour (default)
  - Every 6 hours
  - Every 12 hours
  - Every day
- YAML export functionality with download handler
- Direct download URL: `/api/listing_homeassistant/download`
- Custom Lovelace card for visualization and export
- Sorted and structured YAML export format
- Material Design icons for better UX
- French and English translations
- HACS compatibility
- Comprehensive documentation

### Features

#### Data Collection
- Collects all devices with manufacturer, model, and software version
- Collects all entities with state and attributes
- Groups entities by domain
- Tracks automation states and last triggered times
- Includes all scripts and scenes
- Includes all input entities

#### Export Format
- Hierarchical YAML structure
- Sorted by entity ID and name
- Includes summary statistics
- Timestamp of export
- Full entity details including states and attributes

#### User Interface
- Custom Lovelace card with statistics display
- Refresh button for manual updates
- Export button for one-click YAML download
- Last update timestamp display
- Material Design icons

### Technical Details
- Minimum Home Assistant version: 2023.1.0
- Uses DataUpdateCoordinator for efficient updates
- Async/await for non-blocking operations
- Proper error handling and logging
- Integration with Home Assistant's entity and device registries

### Documentation
- Complete README with installation and usage instructions
- HACS installation guide
- Card documentation
- Example configurations
- Troubleshooting guide
- French translations

[1.0.0]: https://github.com/Turiko313/ListingHomeAssistant/releases/tag/v1.0.0
