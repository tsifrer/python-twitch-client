from twitch.api.base import TwitchAPI
from twitch.constants import (
    BROADCAST_TYPE_HIGHLIGHT, BROADCATS_TYPES, DIRECTIONS, DIRECTION_ASC, DIRECTION_DESC,
    VIDEO_SORTS, VIDEO_SORT_TIME)
from twitch.decorators import oauth_required
from twitch.exceptions import TwitchAttributeException
from twitch.resources import Channel, Community, Follow, Subscription, Team, User, Video


class Channels(TwitchAPI):

    @oauth_required
    def get(self):
        response = self._request_get('channels')
        return Channel.construct_from(response)

    def get_by_id(self, channel_id):
        response = self._request_get('channels/%s' % channel_id)
        return Channel.construct_from(response)

    @oauth_required
    def update(self, channel_id, status=None, game=None, delay=None, channel_feed_enabled=None):

        data = {}
        if status is not None:
            data['status'] = status
        if game is not None:
            data['game'] = game
        if delay is not None:
            data['delay'] = delay
        if channel_feed_enabled is not None:
            data['channel_feed_enabled'] = channel_feed_enabled

        response = self._request_put('channels/%s' % channel_id, data)
        return Channel.construct_from(response)

    @oauth_required
    def get_editors(self, channel_id):
        response = self._request_get('channels/%s/editors' % channel_id)
        return [User.construct_from(x) for x in response['users']]

    def get_followers(self, channel_id, limit=25, offset=0, cursor=None, direction=DIRECTION_DESC):
        if limit > 100:
            raise TwitchAttributeException(
                'Maximum number of objects returned in one request is 100')
        if direction not in DIRECTIONS:
            raise TwitchAttributeException(
                'Direction is not valid. Valid values are %s' % DIRECTIONS)

        params = {
            'limit': limit,
            'offset': offset,
            'direction': direction
        }
        if cursor is not None:
            params['cursor'] = cursor
        response = self._request_get('channels/%s/follows' % channel_id, params=params)
        return [Follow.construct_from(x) for x in response['follows']]

    def get_teams(self, channel_id):
        response = self._request_get('channels/%s/teams' % channel_id)
        return [Team.construct_from(x) for x in response['teams']]

    @oauth_required
    def get_subscribers(self, channel_id, limit=25, offset=0, direction=DIRECTION_ASC):
        if limit > 100:
            raise TwitchAttributeException(
                'Maximum number of objects returned in one request is 100')
        if direction not in DIRECTIONS:
            raise TwitchAttributeException(
                'Direction is not valid. Valid values are %s' % DIRECTIONS)

        response = self._request_get('channels/%s/subscriptions' % channel_id)
        return [Subscription.construct_from(x) for x in response['subscriptions']]

    def check_subscription_by_user(self, channel_id, user_id):
        response = self._request_get('channels/%s/subscriptions/%s' % (channel_id, user_id))
        return Subscription.construct_from(response)

    def get_videos(self, channel_id, limit=10, offset=0, broadcast_type=BROADCAST_TYPE_HIGHLIGHT,
                   language=None, sort=VIDEO_SORT_TIME):
        if limit > 100:
            raise TwitchAttributeException(
                'Maximum number of objects returned in one request is 100')
        if broadcast_type not in BROADCATS_TYPES:
            raise TwitchAttributeException(
                'Broadcast type is not valid. Valid values are %s' % BROADCATS_TYPES)
        if sort not in VIDEO_SORTS:
            raise TwitchAttributeException('Sort is not valid. Valid values are %s' % VIDEO_SORTS)

        params = {
            'limit': limit,
            'offset': offset,
            'broadcast_type': broadcast_type,
            'sort': sort
        }
        if language is not None:
            params['language'] = language
        response = self._request_get('channels/%s/videos' % channel_id, params=params)
        return [Video.construct_from(x) for x in response['videos']]

    @oauth_required
    def start_commercial(self, channel_id, duration=30):
        data = {
            'duration': duration
        }
        response = self._request_post('channels/%s/commercial' % channel_id, data=data)
        return response

    @oauth_required
    def reset_stream_key(self, channel_id):
        response = self._request_delete('channels/%s/stream_key' % channel_id)
        return Channel.construct_from(response)

    def get_community(self, channel_id):
        response = self._request_get('channels/%s/community' % channel_id)
        return Community.construct_from(response)

    def set_community(self, channel_id, community_id):
        self._request_put('channels/%s/community/%s' % (channel_id, community_id))

    def delete_from_community(self, channel_id):
        self._request_delete('channels/%s/community' % channel_id)
