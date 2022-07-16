from twitch.api.base import TwitchAPI
from twitch.resources import Ingest


class Ingests(TwitchAPI):
    async def get_server_list(self):
        response = await self._request_get("ingests")
        return [Ingest.construct_from(x) for x in response["ingests"]]
