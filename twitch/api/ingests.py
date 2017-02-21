from twitch.api.base import TwitchAPI
from twitch.resources import Ingest


class Ingests(TwitchAPI):

    def get_server_list(self):
        response = self._request_get('ingests')
        return [Ingest.construct_from(x) for x in response['ingests']]
