from typing import Optional

from chzzk.client import ChzzkClient, Credential, GameClient
from chzzk.models import Channel, User

__version__ = "0.0.1"


class Chzzk:
    def __init__(self, credential: Optional[Credential] = None):
        self._game_client = GameClient(credential)
        self._chzzk_client = ChzzkClient(credential)

    async def me(self) -> User:
        payload = await self._game_client.get("v1/user/getUserStatus")
        return User(**payload)

    async def channel(self, id: str) -> Channel:
        payload = await self._chzzk_client.get(f"service/v1/channels/{id}")
        return Channel(**payload)
