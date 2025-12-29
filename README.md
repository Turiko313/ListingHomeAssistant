# Listing Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)

Une intégration HACS pour Home Assistant qui liste tous les appareils, entités, automatisations, scènes, scripts, et blueprints de votre instance Home Assistant.

## Fonctionnalités

- 📋 **Liste complète** de tous vos appareils et entités
- 🤖 **Automatisations, scripts et scènes** facilement accessibles
- 🔄 **Actualisation manuelle** via un service
- ⏰ **Actualisation automatique** configurable (toutes les heures, 6 heures, 12 heures ou quotidienne)
- 📤 **Export YAML** avec structure arborescente triée
- 📊 **Sensors dédiés** pour chaque type de données
- 🎨 **Icônes personnalisées** pour une meilleure visualisation

## Installation

### Via HACS (recommandé)

1. Ouvrez HACS dans votre instance Home Assistant
2. Cliquez sur "Integrations"
3. Cliquez sur le menu trois points en haut à droite
4. Sélectionnez "Custom repositories"
5. Ajoutez `https://github.com/Turiko313/ListingHomeAssistant` comme repository
6. Sélectionnez "Integration" comme catégorie
7. Cliquez sur "Add"
8. Recherchez "Listing Home Assistant" et installez-le
9. Redémarrez Home Assistant

### Installation manuelle

1. Téléchargez le dossier `custom_components/listing_homeassistant`
2. Copiez-le dans votre dossier `custom_components` de Home Assistant
3. Redémarrez Home Assistant

## Configuration

1. Allez dans **Paramètres** > **Appareils et services**
2. Cliquez sur **+ Ajouter une intégration**
3. Recherchez **Listing Home Assistant**
4. Suivez les étapes de configuration

### Options

Vous pouvez configurer l'intervalle de mise à jour automatique dans les options de l'intégration :

- Toutes les heures (par défaut)
- Toutes les 6 heures
- Toutes les 12 heures
- Tous les jours

## Utilisation

### Sensors créés

L'intégration crée plusieurs sensors :

- **Devices** : Nombre total d'appareils avec détails
- **Entities** : Nombre total d'entités regroupées par domaine
- **Automations** : Liste des automatisations
- **Scripts** : Liste des scripts
- **Scenes** : Liste des scènes
- **Inputs** : Liste des inputs (input_boolean, input_number, etc.)
- **Summary** : Résumé de toutes les données

### Services

#### listing_homeassistant.refresh

Actualise manuellement les données de listing.

```yaml
service: listing_homeassistant.refresh
```

### Export YAML

Pour exporter les données en YAML, utilisez la carte personnalisée ou accédez directement à l'URL de téléchargement :

```
http://your-home-assistant:8123/api/listing_homeassistant/download
```

Le fichier sera téléchargé automatiquement avec un nom incluant la date et l'heure.

### Carte personnalisée

Une carte Lovelace personnalisée est disponible pour une meilleure visualisation. Voir [CARD_DOCUMENTATION.md](CARD_DOCUMENTATION.md) pour plus de détails.

Pour ajouter la carte :

```yaml
type: custom:listing-homeassistant-card
```

### Exemple d'automatisation

```yaml
automation:
  - alias: "Actualisation quotidienne"
    trigger:
      - platform: time
        at: "00:00:00"
    action:
      - service: listing_homeassistant.refresh
```

### Accès aux données

Toutes les données collectées sont disponibles dans les attributs des sensors. Vous pouvez y accéder via :

- Les cartes d'entités dans le dashboard
- Les templates
- Les automatisations

Exemple de template :

```yaml
{{ state_attr('sensor.listing_home_assistant_summary', 'total_devices') }}
```

## Structure du YAML exporté

Le fichier YAML exporté contient une structure arborescente complète :

```yaml
listing_home_assistant:
  export_date: "2024-01-01T12:00:00"
  summary:
    total_devices: 10
    total_entities: 50
    total_automations: 5
    total_scripts: 3
    total_scenes: 2
  devices:
    - name: "Device 1"
      manufacturer: "Manufacturer"
      model: "Model"
  entities:
    light:
      - entity_id: "light.living_room"
        name: "Living Room"
        state: "on"
    sensor:
      - entity_id: "sensor.temperature"
        name: "Temperature"
        state: "20.5"
  automations:
    - entity_id: "automation.morning_routine"
      name: "Morning Routine"
  scripts:
    - entity_id: "script.bedtime"
      name: "Bedtime"
  scenes:
    - entity_id: "scene.movie"
      name: "Movie"
  inputs:
    input_boolean:
      - entity_id: "input_boolean.guest_mode"
        name: "Guest Mode"
```

## Capture d'écran

![Listing Home Assistant](https://via.placeholder.com/800x400.png?text=Listing+Home+Assistant)

## Support

Pour toute question ou problème, veuillez ouvrir une issue sur [GitHub](https://github.com/Turiko313/ListingHomeAssistant/issues).

## Licence

MIT License - voir le fichier LICENSE pour plus de détails.

## Auteur

[@Turiko313](https://github.com/Turiko313)
