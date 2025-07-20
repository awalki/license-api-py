import httpx
from pydantic import BaseModel
import websockets
import asyncio


class LoginRequest(BaseModel):
    username: str
    password: str
    hwid: str


class LicenseAPI:
    def __init__(self, url):
        """
        Initialize the LicenseAPI with the given URL.

        Args:
            url (str): The base URL of the license API.
        """
        self.url = url
        self.ws_url = f"{self.url.replace('http', 'ws')}/ws/notify"

    async def login(self, creds: LoginRequest) -> bool:
        """
        Login to the license API

        Args:
            creds (LoginRequest): The login credentials.
        """
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.url}/auth/login",
                json=creds
            )

            response.raise_for_status()

        return True
    
    async def connect_to_websocket(self):
        """
        Connect to the WebSocket endpoint of the license API and implement ping.
        """
        try:
            async with websockets.connect(self.ws_url) as ws:
                while True:
                    await asyncio.sleep(30)
                    await ws.ping()
        except Exception as e:
            print(f"Connection error: {e}")
            exit(1)