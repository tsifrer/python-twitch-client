
from twitch.api.base import TwitchAPI
from twitch.constants import BROADCAST_TYPE_HIGHLIGHT, BROADCATS_TYPES, VIDEO_SORTS, VIDEO_SORT_TIME
from twitch.resources import Channel, Video


class Channels(TwitchAPI):

    def get_by_id(self, channel_id):
        # https://devel_b.twitch.tv/docs/v5/reference/channels/#get-channel-by-id
        url = 'channels/%s' % channel_id

        response = self._request_get(url)
        return Channel.construct_from(response)

    def get_videos(self, channel_id, limit=10, offset=0, broadcast_type=BROADCAST_TYPE_HIGHLIGHT,
                   language=None, sort=VIDEO_SORT_TIME):
        assert limit <= 100, 'Maximum number of videos returned in one request is 100'
        assert broadcast_type in BROADCATS_TYPES, (
            'Broadcast type is not valid. Valid values are %s' % BROADCATS_TYPES)
        assert sort in VIDEO_SORTS, 'Sort is not valid. Valid values are %s' % VIDEO_SORTS

        url = 'channels/%s/videos' % channel_id
        response = self._request_get(url)
        return [Video.construct_from(x) for x in response['videos']]

    def get_channel(self):
        # https://dev.twitch.tv/docs/v5/reference/channels/#get-channel
        # TODO: implement it
        raise NotImplementedError

    def update_channel(self):
        # https://dev.twitch.tv/docs/v5/reference/channels/#update-channel
        # TODO: implement it
        raise NotImplementedError

    def get_channel_editors(self):
        # https://dev.twitch.tv/docs/v5/reference/channels/#get-channel-editors
        # TODO: implement it
        raise NotImplementedError

    def get_channel_followers(self):
        # https://dev.twitch.tv/docs/v5/reference/channels/#get-channel-followers
        # TODO: implement it
        raise NotImplementedError

    def get_channel_teams(self):
        # https://dev.twitch.tv/docs/v5/reference/channels/#get-channel-teams
        # TODO: implement it
        raise NotImplementedError

    def get_channel_subscribers(self):
        # https://dev.twitch.tv/docs/v5/reference/channels/#get-channel-subscribers
        # TODO: implement it
        raise NotImplementedError

    def check_channel_subscription_by_user(self):
        # https://dev.twitch.tv/docs/v5/reference/channels/#check-channel-subscription-by-user
        # TODO: implement it
        raise NotImplementedError

    def start_channel_commercial(self):
        # https://dev.twitch.tv/docs/v5/reference/channels/#start-channel-commercial
        # TODO: implement it
        raise NotImplementedError

    def reset_channel_stream_key(self):
        # https://dev.twitch.tv/docs/v5/reference/channels/#reset-channel-stream-key
        # TODO: implement it
        raise NotImplementedError

    def get_channel_community(self):
        # https://dev.twitch.tv/docs/v5/reference/channels/#get-channel-community
        # TODO: implement it
        raise NotImplementedError

    def set_channel_community(self):
        # https://dev.twitch.tv/docs/v5/reference/channels/#set-channel-community
        # TODO: implement it
        raise NotImplementedError

    def delete_channel_from_community(self):
        # https://dev.twitch.tv/docs/v5/reference/channels/#delete-channel-from-community
        # TODO: implement it
        raise NotImplementedError
