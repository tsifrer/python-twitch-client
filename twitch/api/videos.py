from twitch.api.base import TwitchAPI
from twitch.constants import BROADCAST_TYPE_HIGHLIGHT, BROADCAST_TYPES, PERIODS, PERIOD_WEEK, VOD_FETCH_URL
from twitch.decorators import oauth_required
from twitch.exceptions import TwitchAttributeException
from twitch.resources import Video


class Videos(TwitchAPI):

    def get_by_id(self, video_id):
        response = self._request_get('videos/%s' % video_id)
        return Video.construct_from(response)

    def get_top(self, limit=10, offset=0, game=None, period=PERIOD_WEEK,
                broadcast_types=[BROADCAST_TYPE_HIGHLIGHT]):
        if limit > 100:
            raise TwitchAttributeException(
                'Maximum number of objects returned in one request is 100')
        if period not in PERIODS:
            raise TwitchAttributeException('Period is not valid. Valid values are %s' % PERIODS)

        for broadcast_type in broadcast_types:
            if broadcast_type not in BROADCAST_TYPES:
                raise TwitchAttributeException(
                    'Broadcast type is not valid. Valid values are %s' % BROADCAST_TYPES)

        params = {
            'limit': limit,
            'offset': offset,
            'game': game,
            'period': period,
            'broadcast_type': ",".join(broadcast_types)
        }

        response = self._request_get('videos/top', params=params)
        return [Video.construct_from(x) for x in response['vods']]

    @oauth_required
    def get_followed_videos(self, limit=10, offset=0, broadcast_type=broadcast_types):
        if limit > 100:
            raise TwitchAttributeException(
                'Maximum number of objects returned in one request is 100')

        for broadcast_type in broadcast_types:
            if broadcast_type not in BROADCAST_TYPES:
                raise TwitchAttributeException(
                    'Broadcast type is not valid. Valid values are %s' % BROADCAST_TYPES)

        params = {
            'limit': limit,
            'offset': offset,
            'broadcast_type': broadcast_type
        }

        response = self._request_get('videos/followed', params=params)
        return [Video.construct_from(x) for x in response['videos']]

    def download_vod(self, video_id):
        """
        This will return a byte string of the M3U8 playlist data (which contains more links to segments of the vod)
        """
        vod_id = video_id[1:]
        token = self._request_get('vods/%s/access_token' % vod_id, url='https://api.twitch.tv/api/')
        params = {
            'nauthsig': token["sig"],
            'nauth': token["token"]
        }
        m3u8 = self._request_get('vod/%s' % vod_id, url=VOD_FETCH_URL, params=params, json=False)
        return m3u8.content