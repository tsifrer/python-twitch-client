from twitch.api.base import TwitchAPI
from twitch.resources import Channel, Game, Stream


class Search(TwitchAPI):

    def channels(self, query, limit=25, offset=0):
        assert limit <= 100, ('Maximum number of channels returned in one request '
                              'is 100')

        params = {
            'query': query,
            'limit': limit,
            'offset': offset
        }
        response = self._request_get('search/channels', params=params)
        return [Channel.construct_from(x) for x in response['channels']]

    def games(self, query, live=False):
        params = {
            'query': query,
            'live': live,
        }
        response = self._request_get('search/games', params=params)
        return [Game.construct_from(x) for x in response['games']]

    def streams(self, query, limit=25, offset=0, hls=None):
        assert limit <= 100, ('Maximum number of streams returned in one request '
                              'is 100')

        params = {
            'query': query,
            'limit': limit,
            'offset': offset,
            'hls': hls
        }
        response = self._request_get('search/streams', params=params)
        return [Stream.construct_from(x) for x in response['streams']]
