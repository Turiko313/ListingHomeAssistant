# Listing Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)

Une intégration HACS pour Home Assistant qui liste tous les appareils, entités, automatisations, scènes, scripts, et plus de votre instance Home Assistant.

## Nouveautés majeures de la v1.3.1 (Sécurité & Optimisation)

- **CRITICAL FIX**: `sensor.py` n'intègre plus les très longues listes dans ses attributs, ce qui évite l'explosion de la base de données HA et l'erreur d'attributs dépassant les 16 Ko.
- **PERFORMANCE**: La génération YAML (`download.py`) s'effectue dans un thread en arrière-plan (`async_add_executor_job`), garantissant 0 freeze sur l'interface Home Assistant, même sur les gros systèmes !
- **ROBUSTE**: Auto-nettoyage des dictionnaires complexes Home Assistant (datetimes, Enums, `ReadOnlyDicts`, etc) par une sérialisation JSON transitoire. Finis les tags `!!python/object/...` illisibles dans le YAML exporté.
- **AMÉLIORATION Options UI**: Les sélections UI persistantes (Intervalle, Section_à_exporter) ne s'écrasent plus mutuellement.

## Fonctionnalités

- **PERFORMANCE ASSURÉE** : Rendu des exports YAML asynchrones et sécurisés, plus aucune base de données lente à cause d'attributs gigantesques stockés (Optimisation majeure).
- 📋 **Liste complète** de tous vos appareils et entités
- 🤖 **Automatisations, scripts et scènes** avec détails (déclencheurs, conditions, actions, séquences)
- 🔘 **Boutons intégrés** pour actualiser et exporter
- ⏰ **Actualisation automatique** configurable via entité Select
- 📥 **Export YAML ciblé** : choisissez la section à exporter (Tout, Appareils, Automatisations, etc.) via entité Select
- 📤 **Export YAML optimisé** avec structure arborescente triée
- 📊 **11 entités créées** (7 sensors + 2 boutons + 2 selects)
- 🎨 **Interface complète** directement dans Home Assistant

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
5. Les entités seront créées automatiquement

## Entités créées

### Contrôles (4 entités)

#### `button.actualiser_les_donnees`
- 🔄 Actualise manuellement toutes les données
- Icône : `mdi:refresh`

#### `button.exporter_en_yaml`
- 📥 Crée une notification avec le lien de téléchargement YAML selon la section sélectionnée
- Icône : `mdi:download`

#### `select.intervalle_de_mise_a_jour`
- ⏱️ Configure l'intervalle d'actualisation automatique
- Options : Toutes les heures / 6h / 12h / 24h
- Icône : `mdi:timer-cog`

#### `select.section_a_exporter`
- 🎯 Définit la section des données à exporter via le bouton YAML
- Options : Tout (complet), Appareils, Entités, Automatisations, Scripts, Scènes, Entrées, Blueprints
- Icône : `mdi:filter-variant`

### Statistiques (7 sensors)

- **`sensor.listing_home_assistant_summary`** - Résumé global
- **`sensor.listing_home_assistant_devices`** - Liste des appareils
- **`sensor.listing_home_assistant_entities`** - Entités par domaine
- **`sensor.listing_home_assistant_automations`** - Liste des automatisations
- **`sensor.listing_home_assistant_scripts`** - Liste des scripts
- **`sensor.listing_home_assistant_scenes`** - Liste des scènes
- **`sensor.listing_home_assistant_inputs`** - Liste des inputs

## Utilisation

### Exemple de carte Dashboard

```yaml
type: vertical-stack
cards:
  # Contrôles
  - type: entities
    title: 🎛️ Contrôles Listing
    entities:
      - entity: button.actualiser_les_donnees
        name: Actualiser maintenant
      - entity: button.exporter_en_yaml
        name: Télécharger YAML
      - entity: select.intervalle_de_mise_a_jour
        name: Intervalle automatique
        
  # Résumé
  - type: entity
    entity: sensor.listing_home_assistant_summary
    name: 📊 Résumé
    
  # Statistiques détaillées
  - type: glance
    title: 📈 Statistiques détaillées
    entities:
      - sensor.listing_home_assistant_devices
      - sensor.listing_home_assistant_entities
      - sensor.listing_home_assistant_automations
      - sensor.listing_home_assistant_scripts
      - sensor.listing_home_assistant_scenes
      - sensor.listing_home_assistant_inputs
```

### Service

#### listing_homeassistant.refresh

Actualise manuellement les données (équivalent au bouton).

```yaml
service: listing_homeassistant.refresh
```

### Export YAML par Section

Deux méthodes pour exporter vos données ou une section spécifique :

1. **Via l'interface (UI)** :
   - Choisissez un filtre via l'entité `select.section_a_exporter` (ex: "Automatisations").
   - Cliquez sur `button.exporter_en_yaml`, une notification apparaît.
   - Cliquez sur le lien pour télécharger un YAML trié contenant toutes les étapes détaillées (Triggers, Conditions, Actions, etc.).
2. **Via URL directe (API)** :
   - Vous pouvez interroger l'URL avec un paramètre section : `/api/listing_homeassistant/download?section=automations` (Nécessite authentification classique Home Assistant).

### Exemple d'automatisation

```yaml
automation:
  - alias: "Export quotidien automatique"
    trigger:
      - platform: time
        at: "00:00:00"
    action:
      - service: button.press
        target:
          entity_id: button.exporter_en_yaml
```

### Accès aux données dans les templates

```yaml
# Nombre total d'appareils
{{ state_attr('sensor.listing_home_assistant_summary', 'total_devices') }}

# Liste des automatisations
{{ state_attr('sensor.listing_home_assistant_automations', 'automations') }}

# Nombre d'entités par domaine
{{ state_attr('sensor.listing_home_assistant_entities', 'domain_counts') }}
```

## Structure du YAML exporté

```yaml
listing_home_assistant:
  export_date: "2024-12-30T15:00:00"
  summary:
    total_devices: 10
    total_entities: 50
    total_automations: 5
    total_scripts: 3
    total_scenes: 2
    total_inputs: 4
  devices:
    - name: "Device 1"
      manufacturer: "Manufacturer"
      model: "Model"
  entities:
    light:
      - entity_id: "light.living_room"
        name: "Living Room"
        state: "on"
  automations:
    - entity_id: "automation.morning_routine"
      name: "Morning Routine"
      state: "on"
      mode: "single"
      last_triggered: "2024-12-30T06:00:00"
      triggers:
        - platform: time
          at: "06:00:00"
      conditions: []
      actions:
        - service: light.turn_on
          target:
            entity_id: "light.bedroom"
  scripts:
    - entity_id: "script.bedtime"
      name: "Bedtime"
      state: "off"
      mode: "single"
      sequence:
        - service: light.turn_off
          target:
            entity_id: "all"
  scenes:
    - entity_id: "scene.movie"
      name: "Movie"
  inputs:
    input_boolean:
      - entity_id: "input_boolean.guest_mode"
        name: "Guest Mode"
```

## Support

Pour toute question ou problème, veuillez ouvrir une issue sur [GitHub](https://github.com/Turiko313/ListingHomeAssistant/issues).

## Licence

MIT License - voir le fichier LICENSE pour plus de détails.

## Auteur

[@Turiko313](https://github.com/Turiko313)
