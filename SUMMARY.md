# Listing Home Assistant - Summary

## Project Overview

**Listing Home Assistant** is a custom HACS integration for Home Assistant that provides comprehensive listing and export capabilities for all components in a Home Assistant instance.

## Key Features

### 📊 Comprehensive Data Collection
- **Devices**: All registered devices with manufacturer, model, and version info
- **Entities**: All entities grouped by domain (light, sensor, switch, etc.)
- **Automations**: Complete automation list with last triggered timestamp
- **Scripts**: All available scripts
- **Scenes**: All configured scenes
- **Inputs**: All input entities (input_boolean, input_number, input_select, etc.)

### 🔄 Flexible Updates
- **Automatic Refresh**: Configurable intervals (1h, 6h, 12h, 24h)
- **Manual Refresh**: On-demand refresh via service call
- **Efficient Updates**: Uses Home Assistant's DataUpdateCoordinator

### 📤 Export Capabilities
- **YAML Export**: Structured, hierarchical YAML format
- **One-Click Download**: Direct browser download via HTTP endpoint
- **Sorted Output**: All data sorted alphabetically for easy navigation
- **Timestamped Files**: Each export includes timestamp in filename

### 🎨 User Interface
- **Custom Lovelace Card**: Modern, responsive card with statistics
- **Material Design Icons**: Beautiful icons for each data type
- **Action Buttons**: Quick refresh and export buttons
- **Real-time Stats**: Live count of all component types

### 🌍 Internationalization
- **French**: Complete French translation
- **English**: Full English support
- Extensible for additional languages

## Technical Architecture

### Components

1. **Integration Core** (`__init__.py`)
   - DataUpdateCoordinator for data management
   - Service registration
   - Download handler registration

2. **Configuration Flow** (`config_flow.py`)
   - User-friendly setup wizard
   - Options flow for update interval configuration

3. **Sensors** (`sensor.py`)
   - 7 dedicated sensors for different data types
   - Rich attributes with full data details
   - Consistent state and attribute updates

4. **Services** (`services.py`)
   - Manual refresh service
   - Proper error handling

5. **Download Handler** (`download.py`)
   - HTTP view for YAML export
   - Authentication required
   - Dynamic filename generation

6. **Frontend Card** (`www/listing-homeassistant-card.js`)
   - Custom Lovelace card
   - Interactive buttons
   - Real-time statistics display

### Data Flow

```
HA Registries → Coordinator → Sensors → Frontend
                     ↓
              Download Handler → YAML Export
```

## Installation Methods

### HACS (Recommended)
1. Add custom repository: `https://github.com/Turiko313/ListingHomeAssistant`
2. Install via HACS interface
3. Restart Home Assistant
4. Add integration via UI

### Manual
1. Copy `custom_components/listing_homeassistant` to HA config
2. Restart Home Assistant
3. Add integration via UI

## Usage Examples

### View Statistics
```yaml
# View in Lovelace
type: custom:listing-homeassistant-card

# Or use entity cards
type: entities
entities:
  - sensor.listing_home_assistant_summary
  - sensor.listing_home_assistant_devices
  - sensor.listing_home_assistant_entities
```

### Automate Refresh
```yaml
automation:
  - alias: "Daily Refresh"
    trigger:
      platform: time
      at: "00:00:00"
    action:
      service: listing_homeassistant.refresh
```

### Export via URL
```
GET /api/listing_homeassistant/download
```

### Access Data in Templates
```yaml
{{ state_attr('sensor.listing_home_assistant_summary', 'total_devices') }}
{{ state_attr('sensor.listing_home_assistant_entities', 'domain_counts') }}
```

## File Structure

```
ListingHomeAssistant/
├── custom_components/
│   └── listing_homeassistant/
│       ├── __init__.py              # Integration setup
│       ├── config_flow.py           # Configuration UI
│       ├── const.py                 # Constants
│       ├── sensor.py                # Sensor platform
│       ├── services.py              # Service handlers
│       ├── download.py              # YAML export handler
│       ├── manifest.json            # Integration metadata
│       ├── strings.json             # Default strings
│       ├── icons.json               # Icon definitions
│       ├── translations/
│       │   ├── en.json              # English
│       │   └── fr.json              # French
│       └── www/
│           └── listing-homeassistant-card.js  # Custom card
├── README.md                        # Main documentation
├── INSTALLATION.md                  # Installation guide
├── EXAMPLE_CONFIG.md                # Configuration examples
├── CARD_DOCUMENTATION.md            # Card documentation
├── ARCHITECTURE.md                  # Technical architecture
├── CHANGELOG.md                     # Version history
├── LICENSE                          # MIT License
├── hacs.json                        # HACS metadata
└── info.md                          # HACS info

```

## Sensors Created

| Sensor | Description | State | Attributes |
|--------|-------------|-------|------------|
| `sensor.listing_home_assistant_devices` | Device count | Number | Full device list |
| `sensor.listing_home_assistant_entities` | Entity count | Number | Entities by domain |
| `sensor.listing_home_assistant_automations` | Automation count | Number | Full automation list |
| `sensor.listing_home_assistant_scripts` | Script count | Number | Full script list |
| `sensor.listing_home_assistant_scenes` | Scene count | Number | Full scene list |
| `sensor.listing_home_assistant_inputs` | Input count | Number | Inputs by type |
| `sensor.listing_home_assistant_summary` | Summary | "Ready" | All statistics |

## Services Provided

### `listing_homeassistant.refresh`
- **Description**: Manually refresh all listing data
- **Parameters**: None
- **Returns**: None

## Export Format

```yaml
listing_home_assistant:
  export_date: "2024-12-29T22:00:00"
  summary:
    total_devices: 10
    total_entities: 50
    total_automations: 5
    total_scripts: 3
    total_scenes: 2
    total_inputs: 4
  devices:
    - id: "device_1"
      name: "Living Room Light"
      manufacturer: "Philips"
      model: "Hue"
  entities:
    light:
      - entity_id: "light.living_room"
        name: "Living Room"
        state: "on"
  automations:
    - entity_id: "automation.morning"
      name: "Morning Routine"
      last_triggered: "2024-12-29T06:00:00"
  scripts:
    - entity_id: "script.bedtime"
      name: "Bedtime"
  scenes:
    - entity_id: "scene.movie"
      name: "Movie Time"
  inputs:
    input_boolean:
      - entity_id: "input_boolean.guest_mode"
        name: "Guest Mode"
```

## Requirements

- Home Assistant 2023.1.0 or higher
- HACS (recommended for installation)
- Python 3.9+

## Dependencies

- PyYAML 6.0.1 (auto-installed)

## Browser Compatibility

- Chrome/Edge 90+
- Firefox 88+
- Safari 14+

## Performance

- **Initial Load**: < 1 second (typical HA instance)
- **Refresh Time**: < 2 seconds (typical HA instance)
- **Export Time**: < 3 seconds (typical HA instance)
- **Memory Usage**: < 10MB

## Security

- ✅ Requires Home Assistant authentication
- ✅ No external API calls
- ✅ Local data processing only
- ✅ No sensitive data logging

## License

MIT License - See LICENSE file

## Support & Issues

- **Documentation**: See README.md
- **Issues**: https://github.com/Turiko313/ListingHomeAssistant/issues
- **Discussions**: https://github.com/Turiko313/ListingHomeAssistant/discussions

## Credits

**Author**: [@Turiko313](https://github.com/Turiko313)

**Version**: 1.0.0

**Release Date**: December 29, 2024

## Future Enhancements

Potential features for future releases:
- Blueprint listing support
- Area grouping
- CSV export option
- Historical data tracking
- Comparison between exports
- Filter and search capabilities
- Custom export templates
- Integration with HA backup system

## Contribution

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Acknowledgments

- Home Assistant community
- HACS team
- All contributors and testers
