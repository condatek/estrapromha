from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import DOMAIN, CONF_USERNAME, CONF_PASSWORD
from .api import EstraPromAPI

async def async_setup_entry(hass, entry, async_add_entities):
    session = async_get_clientsession(hass)

    api = EstraPromAPI(
        session,
        entry.data[CONF_USERNAME],
        entry.data[CONF_PASSWORD]
    )

    async_add_entities([EstraPromInvoicesSensor(api)], True)

class EstraPromInvoicesSensor(SensorEntity):
    def __init__(self, api):
        self.api = api
        self._attr_name = "Estra Fatture da Pagare"
        self._attr_icon = "mdi:receipt-text"
        self._state = None
        self._invoices = []

    @property
    def state(self):
        return self._state

    @property
    def extra_state_attributes(self):
        return {"invoices": self._invoices}

    async def async_update(self):
        data = await self.api.get_invoices()
        invoices = data.get("invoices", [])
        self._invoices = invoices
        self._state = len(invoices)
