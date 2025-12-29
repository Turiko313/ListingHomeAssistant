class ListingHomeAssistantCard extends HTMLElement {
  set hass(hass) {
    if (!this.content) {
      const card = document.createElement('ha-card');
      card.header = 'Listing Home Assistant';
      this.content = document.createElement('div');
      this.content.style.padding = '16px';
      card.appendChild(this.content);
      this.appendChild(card);
    }

    const domain = 'listing_homeassistant';
    
    // Get all listing sensors
    const devicesSensor = hass.states[`sensor.${domain}_devices`];
    const entitiesSensor = hass.states[`sensor.${domain}_entities`];
    const automationsSensor = hass.states[`sensor.${domain}_automations`];
    const scriptsSensor = hass.states[`sensor.${domain}_scripts`];
    const scenesSensor = hass.states[`sensor.${domain}_scenes`];
    const inputsSensor = hass.states[`sensor.${domain}_inputs`];
    const summarySensor = hass.states[`sensor.${domain}_summary`];

    // Build the UI
    let html = `
      <style>
        .listing-container {
          display: flex;
          flex-direction: column;
          gap: 16px;
        }
        .listing-stats {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
          gap: 12px;
        }
        .stat-card {
          background: var(--card-background-color);
          border: 1px solid var(--divider-color);
          border-radius: 8px;
          padding: 12px;
          text-align: center;
        }
        .stat-icon {
          font-size: 24px;
          margin-bottom: 8px;
        }
        .stat-value {
          font-size: 24px;
          font-weight: bold;
          color: var(--primary-text-color);
        }
        .stat-label {
          font-size: 12px;
          color: var(--secondary-text-color);
          margin-top: 4px;
        }
        .action-buttons {
          display: flex;
          gap: 12px;
          flex-wrap: wrap;
        }
        .action-button {
          flex: 1;
          min-width: 150px;
          padding: 12px 24px;
          background: var(--primary-color);
          color: var(--text-primary-color);
          border: none;
          border-radius: 4px;
          cursor: pointer;
          font-size: 14px;
          font-weight: 500;
          display: flex;
          align-items: center;
          justify-content: center;
          gap: 8px;
        }
        .action-button:hover {
          background: var(--primary-color-dark);
        }
        .action-button ha-icon {
          --mdc-icon-size: 20px;
        }
        .last-update {
          font-size: 12px;
          color: var(--secondary-text-color);
          text-align: center;
          margin-top: 8px;
        }
      </style>
      <div class="listing-container">
        <div class="listing-stats">
    `;

    // Add stat cards
    const stats = [
      { icon: 'mdi:devices', value: devicesSensor?.state || '0', label: 'Appareils' },
      { icon: 'mdi:format-list-bulleted', value: entitiesSensor?.state || '0', label: 'Entités' },
      { icon: 'mdi:robot', value: automationsSensor?.state || '0', label: 'Automatisations' },
      { icon: 'mdi:script-text', value: scriptsSensor?.state || '0', label: 'Scripts' },
      { icon: 'mdi:palette', value: scenesSensor?.state || '0', label: 'Scènes' },
      { icon: 'mdi:form-textbox', value: inputsSensor?.state || '0', label: 'Inputs' },
    ];

    stats.forEach(stat => {
      html += `
        <div class="stat-card">
          <div class="stat-icon">
            <ha-icon icon="${stat.icon}"></ha-icon>
          </div>
          <div class="stat-value">${stat.value}</div>
          <div class="stat-label">${stat.label}</div>
        </div>
      `;
    });

    html += `
        </div>
        <div class="action-buttons">
          <button class="action-button" id="refresh-button">
            <ha-icon icon="mdi:refresh"></ha-icon>
            Actualiser
          </button>
          <button class="action-button" id="export-button">
            <ha-icon icon="mdi:download"></ha-icon>
            Exporter YAML
          </button>
        </div>
    `;

    if (summarySensor?.attributes?.last_update) {
      html += `
        <div class="last-update">
          Dernière mise à jour : ${new Date(summarySensor.attributes.last_update).toLocaleString('fr-FR')}
        </div>
      `;
    }

    html += `</div>`;

    this.content.innerHTML = html;

    // Add event listeners
    const refreshButton = this.content.querySelector('#refresh-button');
    const exportButton = this.content.querySelector('#export-button');

    if (refreshButton) {
      refreshButton.onclick = () => {
        hass.callService(domain, 'refresh', {});
      };
    }

    if (exportButton) {
      exportButton.onclick = async () => {
        // Call the export service
        await hass.callService(domain, 'export_yaml', {});
        
        // Listen for the export ready event
        const removeListener = hass.connection.subscribeEvents((event) => {
          if (event.event_type === `${domain}_yaml_export_ready`) {
            // Get the YAML content from hass.data
            // Since we can't directly access hass.data from the frontend,
            // we'll use a websocket call to get the content
            hass.callWS({
              type: 'call_service',
              domain: domain,
              service: 'get_yaml_export',
            }).then((response) => {
              // For now, show a message that the export is ready
              alert('Export YAML prêt ! Consultez les logs ou utilisez un service pour télécharger le fichier.');
            });
            removeListener();
          }
        }, `${domain}_yaml_export_ready`);
      };
    }
  }

  setConfig(config) {
    // Card configuration
  }

  getCardSize() {
    return 3;
  }
}

customElements.define('listing-homeassistant-card', ListingHomeAssistantCard);

window.customCards = window.customCards || [];
window.customCards.push({
  type: 'listing-homeassistant-card',
  name: 'Listing Home Assistant Card',
  description: 'Une carte pour visualiser et exporter les données de Listing Home Assistant'
});
