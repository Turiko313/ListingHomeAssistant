# Quick Start Guide - Listing Home Assistant

## Installation (5 minutes)

### Via HACS (Recommended)

1. **Open HACS**
   - Navigate to HACS in your Home Assistant sidebar

2. **Add Custom Repository**
   - Click the menu (⋮) → Custom repositories
   - URL: `https://github.com/Turiko313/ListingHomeAssistant`
   - Category: Integration
   - Click Add

3. **Install**
   - Search for "Listing Home Assistant"
   - Click Download
   - Restart Home Assistant

4. **Configure**
   - Settings → Devices & Services → Add Integration
   - Search "Listing Home Assistant"
   - Follow the setup wizard

## First Use (2 minutes)

### Check Your Sensors

Go to Developer Tools → States and search for `listing_home_assistant`:

You should see 7 new sensors:
- `sensor.listing_home_assistant_devices`
- `sensor.listing_home_assistant_entities`
- `sensor.listing_home_assistant_automations`
- `sensor.listing_home_assistant_scripts`
- `sensor.listing_home_assistant_scenes`
- `sensor.listing_home_assistant_inputs`
- `sensor.listing_home_assistant_summary`

### Add to Dashboard

1. **Add the Custom Card**
   
   Go to Settings → Dashboards → Resources → Add Resource:
   - URL: `/listing_homeassistant/listing-homeassistant-card.js`
   - Type: JavaScript Module

2. **Create a Card**
   
   Edit your dashboard and add:
   ```yaml
   type: custom:listing-homeassistant-card
   ```

3. **Done!**
   
   You'll see a beautiful card showing all your statistics with Refresh and Export buttons.

## Basic Usage

### View Statistics

Your card shows:
- 📱 Total devices
- 📊 Total entities
- 🤖 Total automations
- 📝 Total scripts
- 🎨 Total scenes
- 📥 Total inputs

### Manual Refresh

Click the **Actualiser** (Refresh) button on the card, or call the service:

```yaml
service: listing_homeassistant.refresh
```

### Export YAML

Click the **Exporter YAML** button on the card.

Your browser will download a file like:
```
listing_homeassistant_20241229_220000.yaml
```

The file contains all your Home Assistant data in a clean, organized format!

## Configuration Options

To change the auto-refresh interval:

1. Settings → Devices & Services
2. Find "Listing Home Assistant"
3. Click Configure
4. Select your preferred interval:
   - Every hour (default)
   - Every 6 hours
   - Every 12 hours
   - Every day

## Using the Data

### In Templates

```yaml
# Get total device count
{{ states('sensor.listing_home_assistant_devices') }}

# Get all entity domains
{{ state_attr('sensor.listing_home_assistant_summary', 'entity_domains') }}

# Get automation count
{{ states('sensor.listing_home_assistant_automations') }}
```

### In Automations

```yaml
automation:
  - alias: "Alert on new device"
    trigger:
      - platform: state
        entity_id: sensor.listing_home_assistant_devices
    action:
      - service: notify.mobile_app
        data:
          message: "Device count changed to {{ states('sensor.listing_home_assistant_devices') }}"
```

### In Lovelace

Simple entity card:
```yaml
type: entities
entities:
  - sensor.listing_home_assistant_summary
  - sensor.listing_home_assistant_devices
  - sensor.listing_home_assistant_entities
```

Grid layout:
```yaml
type: grid
columns: 3
cards:
  - type: entity
    entity: sensor.listing_home_assistant_devices
  - type: entity
    entity: sensor.listing_home_assistant_entities
  - type: entity
    entity: sensor.listing_home_assistant_automations
```

## Troubleshooting

### Sensors not appearing?

1. Check Settings → Devices & Services
2. Verify "Listing Home Assistant" is installed
3. Restart Home Assistant
4. Check logs for errors

### Card not showing?

1. Verify resource is added (Settings → Dashboards → Resources)
2. Clear browser cache (Ctrl+F5)
3. Check browser console (F12) for errors

### Export not working?

1. Make sure you're logged in to Home Assistant
2. Check browser console for errors
3. Try accessing `/api/listing_homeassistant/download` directly

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Check [EXAMPLE_CONFIG.md](EXAMPLE_CONFIG.md) for advanced configurations
- Review [CARD_DOCUMENTATION.md](CARD_DOCUMENTATION.md) for card customization

## Support

Need help?
- 📖 [Full Documentation](README.md)
- 🐛 [Report Issues](https://github.com/Turiko313/ListingHomeAssistant/issues)
- 💬 [Discussions](https://github.com/Turiko313/ListingHomeAssistant/discussions)

---

**Enjoy your organized Home Assistant data! 🎉**
