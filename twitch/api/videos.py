from twitch.api.base import TwitchAPI
from twitch.constants import BROADCAST_TYPE_HIGHLIGHT, BROADCATS_TYPES, PERIODS, PERIOD_WEEK
from twitch.decorators import oauth_required
from twitch.exceptions import TwitchAttributeException
from twitch.resources import Video


class Videos(TwitchAPI):

    def get_by_id(self, video_id):
        response = self._request_get('videos/%s' % video_id)
        return Video.construct_from(response)

    def get_top(self, limit=10, offset=0, game=None, period=PERIOD_WEEK,
                broadcast_type=BROADCAST_TYPE_HIGHLIGHT):
        if limit > 100:
            raise TwitchAttributeException(
                'Maximum number of objects returned in one request is 100')
        if period not in PERIODS:
            raise TwitchAttributeException('Period is not valid. Valid values are %s' % PERIODS)
        if broadcast_type not in BROADCATS_TYPES:
            raise TwitchAttributeException(
                'Broadcast type is not valid. Valid values are %s' % BROADCATS_TYPES)

        params = {
            'limit': limit,
            'offset': offset,
            'game': game,
            'period': period,
            'broadcast_type': broadcast_type
        }

        response = self._request_get('videos/top', params=params)
        return [Video.construct_from(x) for x in response['vods']]

    @oauth_required
    def get_followed_videos(self, limit=10, offset=0, broadcast_type=BROADCAST_TYPE_HIGHLIGHT):
        if limit > 100:
            raise TwitchAttributeException(
                'Maximum number of objects returned in one request is 100')
        if broadcast_type not in BROADCATS_TYPES:
            raise TwitchAttributeException(
                'Broadcast type is not valid. Valid values are %s' % BROADCATS_TYPES)

        params = {
            'limit': limit,
            'offset': offset,
            'broadcast_type': broadcast_type
        }

        response = self._request_get('videos/followed', params=params)
        return [Video.construct_from(x) for x in response['videos']]
