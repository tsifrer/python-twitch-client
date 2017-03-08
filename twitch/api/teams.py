from twitch.api.base import TwitchAPI
from twitch.exceptions import TwitchAttributeException
from twitch.resources import Team


class Teams(TwitchAPI):

    def get(self, team_name):
        response = self._request_get('teams/%s' % team_name)
        return Team.construct_from(response)

    def get_all(self, limit=10, offset=0):
        if limit > 100:
            raise TwitchAttributeException(
                'Maximum number of objects returned in one request is 100')

        params = {
            'limit': limit,
            'offset': offset
        }
        response = self._request_get('teams', params=params)
        return [Team.construct_from(x) for x in response['teams']]
