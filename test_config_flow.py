"""Test si le config_flow est bien chargé."""
from custom_components.listing_homeassistant import config_flow

print("Version du config_flow:", config_flow.__file__)
print("Classe trouvée:", config_flow.ListingHomeAssistantConfigFlow)
print("DOMAIN:", config_flow.DOMAIN)
