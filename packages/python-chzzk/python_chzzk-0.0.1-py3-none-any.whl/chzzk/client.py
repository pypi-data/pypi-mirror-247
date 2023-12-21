from dataclasses import dataclass
from typing import Any, ClassVar, Optional
from urllib.parse import urljoin

import httpx

from chzzk.errors import ChzzkError


@dataclass
class Credential:
    nid_auth: str
    nid_session: str

    def as_cookie(self) -> dict[str, str]:
        return {
            "NID_AUT": self.nid_auth,
            "NID_SES": self.nid_session,
        }


class HTTPClient:
    BASE_URL: ClassVar[str]

    def __init__(self, credential: Optional[Credential] = None):
        self._credential = credential
        self._client = httpx.AsyncClient()

        if self._credential is not None:
            self._client.cookies.update(self._credential.as_cookie())

    async def request(
        self,
        method: str,
        url: str,
        params: Optional[dict[str, Any]] = None,
        data: Optional[dict[str, Any]] = None,
        *args,
        **kwargs,
    ) -> Any:
        response = await self._client.request(
            method=method,
            url=urljoin(self.BASE_URL, url),
            params=params,
            data=data,
            *args,
            **kwargs,
        )

        if response.status_code != 200:
            raise ChzzkError(f"Status code {response.status_code}")

        payload = response.json()
        if payload["code"] != 200:
            raise ChzzkError(f"Status code {payload['code']}")

        return payload["content"]

    def get(
        self,
        url: str,
        params: Optional[dict[str, Any]] = None,
        data: Optional[dict[str, Any]] = None,
        *args,
        **kwargs,
    ) -> Any:
        return self.request(
            url=url,
            method="get",
            params=params,
            data=data,
            *args,
            **kwargs,
        )

    def post(
        self,
        url: str,
        params: Optional[dict[str, Any]] = None,
        data: Optional[dict[str, Any]] = None,
        *args,
        **kwargs,
    ) -> Any:
        return self.request(
            url=url,
            method="post",
            params=params,
            data=data,
            *args,
            **kwargs,
        )


class GameClient(HTTPClient):
    BASE_URL = "https://comm-api.game.naver.com/nng_main/"

    def __init__(self, credential: Optional[Credential] = None):
        super().__init__(credential)


class ChzzkClient(HTTPClient):
    BASE_URL = "https://api.chzzk.naver.com/"

    def __init__(self, credential: Optional[Credential] = None):
        super().__init__(credential)
