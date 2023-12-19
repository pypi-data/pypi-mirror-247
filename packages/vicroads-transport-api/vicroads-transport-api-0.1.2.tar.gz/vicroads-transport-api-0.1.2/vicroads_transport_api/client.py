from concurrent.futures import ThreadPoolExecutor
import aiohttp
from .errors import *


class DataExchangeClient:
    BASE_URL = "https://data-exchange-api.vicroads.vic.gov.au"

    def __init__(self, sub_key: str):
        self.headers = {"Ocp-Apim-Subscription-Key": sub_key}

    async def get(self, path: str):
        async with aiohttp.ClientSession() as client:
            async with client.get(
                f"{self.BASE_URL}/{path}", headers=self.headers
            ) as response:
                if response.status == 200:
                    return await response.content.read()
                else:
                    self._handle_error(response.status)

    def _handle_error(self, resp: int) -> Exception:
        match resp:
            case 400:
                raise InvalidRequestError()
            case 401:
                raise AccessDeniedError()
            case 404:
                raise NotFoundError()
            case other:
                raise UnknownError()
