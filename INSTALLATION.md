# Guide d'installation de Listing Home Assistant

## Prérequis

- Home Assistant 2023.1.0 ou supérieur
- HACS installé (optionnel mais recommandé)

## Installation via HACS (Recommandé)

1. Ouvrez HACS dans votre instance Home Assistant
2. Cliquez sur **Integrations**
3. Cliquez sur le menu **⋮** (trois points verticaux) en haut à droite
4. Sélectionnez **Custom repositories**
5. Dans le champ **Repository**, entrez : `https://github.com/Turiko313/ListingHomeAssistant`
6. Dans le champ **Category**, sélectionnez : **Integration**
7. Cliquez sur **Add**
8. Fermez la fenêtre des dépôts personnalisés
9. Cliquez sur **+ Explore & Download Repositories**
10. Recherchez **Listing Home Assistant**
11. Cliquez sur **Download**
12. Redémarrez Home Assistant

## Installation manuelle

1. Téléchargez la dernière version depuis [GitHub](https://github.com/Turiko313/ListingHomeAssistant)
2. Extrayez l'archive
3. Copiez le dossier `custom_components/listing_homeassistant` dans le dossier `custom_components` de votre configuration Home Assistant
   - Si le dossier `custom_components` n'existe pas, créez-le à la racine de votre configuration
4. Redémarrez Home Assistant

## Configuration de l'intégration

1. Allez dans **Paramètres** → **Appareils et services**
2. Cliquez sur **+ Ajouter une intégration**
3. Recherchez **Listing Home Assistant**
4. Cliquez sur l'intégration pour l'ajouter
5. Suivez les instructions à l'écran

### Configuration des options

Après l'installation, vous pouvez configurer les options :

1. Allez dans **Paramètres** → **Appareils et services**
2. Trouvez **Listing Home Assistant** dans la liste
3. Cliquez sur **Configurer**
4. Sélectionnez l'intervalle de mise à jour automatique :
   - **Toutes les heures** (par défaut) : 3600 secondes
   - **Toutes les 6 heures** : 21600 secondes
   - **Toutes les 12 heures** : 43200 secondes
   - **Tous les jours** : 86400 secondes

## Installation de la carte personnalisée

La carte personnalisée permet d'avoir une interface visuelle pour consulter et exporter les données.

### Méthode automatique (recommandée)

La carte est automatiquement disponible à l'URL `/listing_homeassistant/listing-homeassistant-card.js`

1. Allez dans **Paramètres** → **Tableaux de bord**
2. Cliquez sur le menu **⋮** en haut à droite
3. Sélectionnez **Ressources**
4. Cliquez sur **+ Ajouter une ressource**
5. Entrez l'URL : `/listing_homeassistant/listing-homeassistant-card.js`
6. Sélectionnez le type : **Module JavaScript**
7. Cliquez sur **Créer**

### Ajout de la carte au tableau de bord

1. Allez sur votre tableau de bord
2. Cliquez sur **Modifier le tableau de bord**
3. Cliquez sur **+ Ajouter une carte**
4. Recherchez **Listing Home Assistant Card**
5. Ajoutez la carte

Ou ajoutez manuellement en mode YAML :

```yaml
type: custom:listing-homeassistant-card
```

## Vérification de l'installation

Après l'installation et la configuration, vous devriez voir les entités suivantes :

- `sensor.listing_home_assistant_devices`
- `sensor.listing_home_assistant_entities`
- `sensor.listing_home_assistant_automations`
- `sensor.listing_home_assistant_scripts`
- `sensor.listing_home_assistant_scenes`
- `sensor.listing_home_assistant_inputs`
- `sensor.listing_home_assistant_summary`

Pour vérifier :

1. Allez dans **Outils de développement** → **États**
2. Recherchez `listing_home_assistant`
3. Vous devriez voir toutes les entités listées ci-dessus

## Services disponibles

L'intégration fournit le service suivant :

### listing_homeassistant.refresh

Force une actualisation immédiate des données.

Utilisation dans une automatisation :

```yaml
service: listing_homeassistant.refresh
```

## Export des données

Pour exporter les données en YAML :

### Via la carte personnalisée

1. Ouvrez votre tableau de bord avec la carte Listing Home Assistant
2. Cliquez sur le bouton **Exporter YAML**
3. Le fichier sera téléchargé automatiquement

### Via l'URL directe

Accédez à l'URL suivante dans votre navigateur :

```
http://VOTRE_ADRESSE_HOME_ASSISTANT:8123/api/listing_homeassistant/download
```

Note : Vous devez être authentifié dans Home Assistant.

## Dépannage

### L'intégration n'apparaît pas dans la liste

1. Vérifiez que le dossier est bien dans `custom_components/listing_homeassistant`
2. Vérifiez les permissions du dossier
3. Redémarrez Home Assistant
4. Consultez les logs : **Paramètres** → **Système** → **Logs**

### Les entités ne sont pas créées

1. Vérifiez que l'intégration est bien configurée dans **Appareils et services**
2. Utilisez le service `listing_homeassistant.refresh` pour forcer une actualisation
3. Consultez les logs pour des erreurs

### La carte personnalisée ne s'affiche pas

1. Vérifiez que la ressource est bien ajoutée dans les ressources du tableau de bord
2. Videz le cache du navigateur (Ctrl+F5 ou Cmd+Shift+R)
3. Vérifiez les erreurs dans la console du navigateur (F12)
4. Assurez-vous que l'URL de la ressource est correcte : `/listing_homeassistant/listing-homeassistant-card.js`

### L'export YAML ne fonctionne pas

1. Vérifiez que vous êtes bien authentifié
2. Essayez d'utiliser l'URL directe : `/api/listing_homeassistant/download`
3. Consultez les logs de Home Assistant pour des erreurs

## Mise à jour

### Via HACS

1. Ouvrez HACS
2. Allez dans **Integrations**
3. Trouvez **Listing Home Assistant**
4. Si une mise à jour est disponible, cliquez sur **Update**
5. Redémarrez Home Assistant

### Manuellement

1. Téléchargez la nouvelle version
2. Remplacez le dossier `custom_components/listing_homeassistant`
3. Redémarrez Home Assistant

## Désinstallation

1. Allez dans **Paramètres** → **Appareils et services**
2. Trouvez **Listing Home Assistant**
3. Cliquez sur le menu **⋮** (trois points)
4. Sélectionnez **Supprimer**
5. Confirmez la suppression
6. Supprimez le dossier `custom_components/listing_homeassistant`
7. Redémarrez Home Assistant

## Support

Pour toute question ou problème :

- Consultez la [documentation complète](README.md)
- Consultez les [exemples de configuration](EXAMPLE_CONFIG.md)
- Ouvrez une [issue sur GitHub](https://github.com/Turiko313/ListingHomeAssistant/issues)
