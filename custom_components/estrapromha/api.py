import aiohttp
import async_timeout

import logging
_LOGGER = logging.getLogger(__name__)


BASE_URL = "https://apiprod2020.estra.it/uca"

class EstraPromAPI:
    def __init__(self, session, username, password):
        self.session = session
        self.username = username
        self.password = password
        self.token = None

    async def login(self):
        url = f"{BASE_URL}/login/v1.0.0/in/"
        payload = {"username": self.username, "password": self.password}

        async with async_timeout.timeout(20):
            async with self.session.post(url, json=payload) as resp:
                data = await resp.json()
                self.token = data.get("access_token")
                return self.token

    async def get_invoices(self):
        """Fetch invoices to pay from Estra API. Returns a list or None on failure."""
        if not self.token:
            await self.login()

        url = f"{BASE_URL}/invoices/v1.0.0/toPayCustomer"
        headers = {"Authorization": f"Bearer {self.token}"}

        try:
            async with async_timeout.timeout(20):
                async with self.session.post(url, json={}, headers=headers) as resp:
                    status = resp.status
                    data = await resp.json()

                    if status != 200:
                        _LOGGER.error(
                            "Error fetching invoices: HTTP %s, response: %s",
                            status,
                            data,
                        )
                        return None

                    if not data.get("success"):
                        _LOGGER.error(
                            "Estra API returned error while fetching invoices: %s",
                            data,
                        )
                        return None

                    invoices = data.get("invoices")
                    if invoices is None:
                        _LOGGER.warning(
                            "Estra API returned success but no 'invoices' field: %s",
                            data,
                        )
                        return None

                    return invoices

        except Exception as e:
            _LOGGER.exception("Unexpected error while fetching invoices: %s", e)
            return None
