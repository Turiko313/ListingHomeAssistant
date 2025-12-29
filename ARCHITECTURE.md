# Architecture de Listing Home Assistant

## Vue d'ensemble

```
┌─────────────────────────────────────────────────────────────┐
│                    Home Assistant                            │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  Listing Home Assistant Integration                     │ │
│  ├────────────────────────────────────────────────────────┤ │
│  │                                                          │ │
│  │  ┌──────────────────────────────────────────────────┐  │ │
│  │  │  ListingDataUpdateCoordinator                     │  │ │
│  │  │  - Collecte les données toutes les X heures      │  │ │
│  │  │  - Accède aux registres d'entités et d'appareils │  │ │
│  │  └──────────────────────────────────────────────────┘  │ │
│  │                        │                                 │ │
│  │                        ▼                                 │ │
│  │  ┌──────────────────────────────────────────────────┐  │ │
│  │  │  Sensors                                          │  │ │
│  │  │  - sensor.listing_home_assistant_devices          │  │ │
│  │  │  - sensor.listing_home_assistant_entities         │  │ │
│  │  │  - sensor.listing_home_assistant_automations      │  │ │
│  │  │  - sensor.listing_home_assistant_scripts          │  │ │
│  │  │  - sensor.listing_home_assistant_scenes           │  │ │
│  │  │  - sensor.listing_home_assistant_inputs           │  │ │
│  │  │  - sensor.listing_home_assistant_summary          │  │ │
│  │  └──────────────────────────────────────────────────┘  │ │
│  │                                                          │ │
│  │  ┌──────────────────────────────────────────────────┐  │ │
│  │  │  Services                                         │  │ │
│  │  │  - listing_homeassistant.refresh                  │  │ │
│  │  └──────────────────────────────────────────────────┘  │ │
│  │                                                          │ │
│  │  ┌──────────────────────────────────────────────────┐  │ │
│  │  │  Download Handler                                 │  │ │
│  │  │  - /api/listing_homeassistant/download            │  │ │
│  │  │  - Génère et télécharge le YAML                   │  │ │
│  │  └──────────────────────────────────────────────────┘  │ │
│  │                                                          │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                               │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  Frontend                                               │ │
│  ├────────────────────────────────────────────────────────┤ │
│  │                                                          │ │
│  │  ┌──────────────────────────────────────────────────┐  │ │
│  │  │  Custom Lovelace Card                             │  │ │
│  │  │  - Affiche les statistiques                       │  │ │
│  │  │  - Bouton Actualiser                              │  │ │
│  │  │  - Bouton Exporter YAML                           │  │ │
│  │  └──────────────────────────────────────────────────┘  │ │
│  │                                                          │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

## Flux de données

### 1. Collecte des données

```
Home Assistant Registries
         │
         ▼
ListingDataUpdateCoordinator
    │    │    │
    ▼    ▼    ▼
Devices  Entities  States
    │    │    │
    └────┴────┘
         │
         ▼
   Données collectées
```

### 2. Mise à jour des sensors

```
Données collectées
         │
         ▼
  Update Coordinator
         │
    ┌────┴────┬────────┬──────┬─────────┬────────┬────────┐
    ▼         ▼        ▼      ▼         ▼        ▼        ▼
Devices  Entities  Automations Scripts  Scenes  Inputs  Summary
Sensor    Sensor     Sensor    Sensor   Sensor  Sensor  Sensor
```

### 3. Export YAML

```
Utilisateur clique sur "Exporter"
         │
         ▼
Frontend appelle /api/listing_homeassistant/download
         │
         ▼
Download Handler récupère les données du Coordinator
         │
         ▼
Génération du YAML avec structure arborescente
         │
         ▼
Téléchargement du fichier
```

## Structure des fichiers

```
custom_components/listing_homeassistant/
├── __init__.py                 # Point d'entrée, setup de l'intégration
├── manifest.json               # Métadonnées de l'intégration
├── config_flow.py              # Configuration UI
├── const.py                    # Constantes
├── sensor.py                   # Définition des sensors
├── services.py                 # Services (refresh)
├── services.yaml               # Définition des services
├── download.py                 # Handler de téléchargement YAML
├── panel.py                    # Enregistrement du panel (non utilisé)
├── strings.json                # Traductions par défaut
├── icons.json                  # Icônes personnalisées
├── translations/
│   ├── en.json                 # Traductions anglaises
│   └── fr.json                 # Traductions françaises
└── www/
    └── listing-homeassistant-card.js  # Carte Lovelace personnalisée
```

## Flux de configuration

```
1. Installation
   └─> Copie des fichiers dans custom_components/

2. Redémarrage de Home Assistant
   └─> Chargement de l'intégration

3. Ajout via UI
   └─> Config Flow
       └─> Création de l'entrée de configuration

4. Setup de l'intégration
   ├─> Création du Coordinator
   ├─> Création des Sensors
   ├─> Enregistrement des Services
   └─> Enregistrement du Download Handler

5. Premier refresh
   └─> Collecte initiale des données

6. Mise à jour automatique
   └─> Basé sur l'intervalle configuré
```

## Interactions utilisateur

### Actualisation manuelle

```
Utilisateur
    │
    ├─> Clique sur "Actualiser" dans la carte
    │   └─> Appel à listing_homeassistant.refresh
    │       └─> Coordinator.async_refresh()
    │           └─> Mise à jour de tous les sensors
    │
    └─> Ou appelle le service dans une automatisation
```

### Export YAML

```
Utilisateur
    │
    ├─> Clique sur "Exporter YAML" dans la carte
    │   └─> Fetch vers /api/listing_homeassistant/download
    │       ├─> Download Handler récupère les données
    │       ├─> Génère le YAML
    │       └─> Retourne le fichier
    │
    └─> Ou accède directement à l'URL
        └─> /api/listing_homeassistant/download
```

## Données collectées

### Devices
```yaml
- id: "device_id"
  name: "Device Name"
  manufacturer: "Manufacturer"
  model: "Model"
  sw_version: "1.0.0"
  area_id: "area_id"
```

### Entities (par domaine)
```yaml
light:
  - entity_id: "light.living_room"
    name: "Living Room"
    device_id: "device_id"
    platform: "hue"
    state: "on"
    attributes: {...}
```

### Automations
```yaml
- entity_id: "automation.morning"
  name: "Morning Routine"
  state: "on"
  last_triggered: "2024-12-29T10:00:00"
```

### Scripts, Scenes, Inputs
```yaml
# Format similaire avec entity_id, name, state
```
