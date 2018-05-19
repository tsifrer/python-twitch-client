from twitch.api.base import TwitchAPI
from twitch.constants import PERIODS
from twitch.decorators import oauth_required
from twitch.exceptions import TwitchAttributeException
from twitch.resources import Clip


class Clips(TwitchAPI):

    def get_by_slug(self, slug):
        response = self._request_get('clips/{}'.format(slug))
        return Clip.construct_from(response)

    def get_top(
            self, channel=None, cursor=None, game=None,
            language=None, limit=10, period='week', trending=False
    ):
        if limit > 100:
            raise TwitchAttributeException(
                'Maximum number of objects returned in one request is 100')

        if period not in PERIODS:
            raise TwitchAttributeException(
                'Period is not valid. Valid values are {}'.format(PERIODS))

        params = {
            'channel': channel,
            'cursor': cursor,
            'game': game,
            'language': language,
            'limit': limit,
            'period': period,
            'trending': str(trending).lower()
        }

        response = self._request_get('clips/top', params=params)
        return [Clip.construct_from(x) for x in response['clips']]

    @oauth_required
    def followed(self, limit=10, cursor=None, trending=False):
        if limit > 100:
            raise TwitchAttributeException(
                'Maximum number of objects returned in one request is 100')

        params = {
            'limit': limit,
            'cursor': cursor,
            'trending': trending
        }

        response = self._request_get('clips/followed', params=params)
        return [Clip.construct_from(x) for x in response['clips']]
