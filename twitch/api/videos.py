from twitch.api.base import TwitchAPI
from twitch.constants import BROADCAST_TYPE_HIGHLIGHT, BROADCATS_TYPES, PERIODS, PERIOD_WEEK
from twitch.resources import Video


class Videos(TwitchAPI):

    def get_by_id(self, video_id):
        response = self._request_get('videos/%s' % video_id)
        return Video.construct_from(response)

    def get_top(self, limit=10, offset=0, game=None, period=PERIOD_WEEK,
                broadcast_type=BROADCAST_TYPE_HIGHLIGHT):
        assert limit <= 100, 'Maximum number of videos returned in one request is 100'
        assert period in PERIODS, 'Period is not valid. Valid values are %s' % PERIODS
        assert broadcast_type in BROADCATS_TYPES, (
            'Broadcast type is not valid. Valid values are %s' % BROADCATS_TYPES)

        response = self._request_get('videos/top')
        return [Video.construct_from(x) for x in response['vods']]

    def get_followed_videos(self, limit=10, offset=0, broadcast_type=BROADCAST_TYPE_HIGHLIGHT):
        assert limit <= 100, 'Maximum number of videos returned in one request is 100'
        assert broadcast_type in BROADCATS_TYPES, (
            'Broadcast type is not valid. Valid values are %s' % BROADCATS_TYPES)

        response = self._request_get('videos/followed')
        return [Video.construct_from(x) for x in response['videos']]
