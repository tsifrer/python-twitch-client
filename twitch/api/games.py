from twitch.api.base import TwitchAPI
from twitch.resources import Game


class Games(TwitchAPI):

    def get_top(self, limit=10, offset=0):
        # https://dev.twitch.tv/docs/v5/reference/games/#get-top-games
        assert limit <= 100, ('Maximum number of games returned in one request '
                              'is 100')

        params = {
            'limit': limit,
            'offset': offset
        }
        response = self._request_get('games/top', params=params)
        return [Game.construct_from(x) for x in response['top']]
