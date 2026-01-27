import aiohttp
import async_timeout

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
        if not self.token:
            await self.login()

        url = f"{BASE_URL}/invoices/v1.0.0/toPayCustomer"
        headers = {"Authorization": f"Bearer {self.token}"}

        async with async_timeout.timeout(20):
            async with self.session.post(url, json={}, headers=headers) as resp:
                return await resp.json()
