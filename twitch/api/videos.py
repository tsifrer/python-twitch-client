from twitch.api.base import TwitchAPI
from twitch.constants import BROADCAST_TYPE_HIGHLIGHT, BROADCATS_TYPES, PERIODS, PERIOD_WEEK
from twitch.resources import Video


class Videos(TwitchAPI):

    def get_by_id(self, video_id):
        # https://dev.twitch.tv/docs/v5/reference/videos/#get-video
        url = 'videos/%s' % video_id

        response = self._request_get(url)
        return Video.construct_from(response)

    def get_top(self, limit=10, offset=0, game=None, period=PERIOD_WEEK,
                broadcast_type=BROADCAST_TYPE_HIGHLIGHT):
        # https://dev.twitch.tv/docs/v5/reference/videos/#get-top-videos
        assert limit <= 100, 'Maximum number of videos returned in one request is 100'
        assert period in PERIODS, 'Period is not valid. Valid values are %s' % PERIODS
        assert broadcast_type in BROADCATS_TYPES, (
            'Broadcast type is not valid. Valid values are %s' % BROADCATS_TYPES)

        url = 'videos/top'
        response = self._request_get(url)

        return [Video.construct_from(x) for x in response['vods']]

    def get_followed_videos(self, limit=10, offset=0, broadcast_type=BROADCAST_TYPE_HIGHLIGHT):
        # https://dev.twitch.tv/docs/v5/reference/videos/#get-followed-videos
        assert limit <= 100, 'Maximum number of videos returned in one request is 100'
        assert broadcast_type in BROADCATS_TYPES, (
            'Broadcast type is not valid. Valid values are %s' % BROADCATS_TYPES)

        url = 'videos/followed'
        response = self._request_get(url)

        return [Video.construct_from(x) for x in response['videos']]
