from twitch.api.base import TwitchAPI
from twitch.constants import DIRECTIONS, DIRECTION_DESC, USERS_SORT_BY, USERS_SORT_BY_CREATED_AT
from twitch.decorators import oauth_required
from twitch.exceptions import TwitchAttributeException
from twitch.resources import Follow, Subscription, User, UserBlock


class Users(TwitchAPI):

    @oauth_required
    def get(self):
        response = self._request_get('user')
        return User.construct_from(response)

    def get_by_id(self, user_id):
        response = self._request_get('users/%s' % user_id)
        return User.construct_from(response)

    @oauth_required
    def get_emotes(self, user_id):
        response = self._request_get('users/%s/emotes' % user_id)
        return response['emoticon_sets']

    @oauth_required
    def check_subscribed_to_channel(self, user_id, channel_id):
        response = self._request_get('users/%s/subscriptions/%s' % (user_id, channel_id))
        return Subscription.construct_from(response)

    def get_follows(self, user_id, limit=25, offset=0, direction=DIRECTION_DESC,
                    sort_by=USERS_SORT_BY_CREATED_AT):
        if limit > 100:
            raise TwitchAttributeException(
                'Maximum number of objects returned in one request is 100')
        if direction not in DIRECTIONS:
            raise TwitchAttributeException(
                'Direction is not valid. Valid values are %s' % DIRECTIONS)
        if sort_by not in USERS_SORT_BY:
            raise TwitchAttributeException(
                'Sort by is not valud. Valid values are %s' % USERS_SORT_BY)

        params = {
            'limit': limit,
            'offset': offset,
            'direction': direction
        }
        response = self._request_get('users/%s/follows/channels' % user_id, params=params)
        return [Follow.construct_from(x) for x in response['follows']]

    def check_follows_channel(self, user_id, channel_id):
        response = self._request_get('users/%s/follows/channels/%s' % (user_id, channel_id))
        return Follow.construct_from(response)

    @oauth_required
    def follow_channel(self, user_id, channel_id, notifications=False):
        data = {
            'notifications': notifications
        }
        response = self._request_put('users/%s/follows/channels/%s' % (user_id, channel_id), data)
        return Follow.construct_from(response)

    @oauth_required
    def unfollow_channel(self, user_id, channel_id):
        self._request_delete('users/%s/follows/channels/%s' % (user_id, channel_id))

    @oauth_required
    def get_user_block_list(self, user_id, limit=25, offset=0):
        if limit > 100:
            raise TwitchAttributeException(
                'Maximum number of objects returned in one request is 100')

        params = {
            'limit': limit,
            'offset': offset
        }
        response = self._request_get('users/%s/blocks' % user_id, params=params)
        return [UserBlock.construct_from(x) for x in response['blocks']]

    @oauth_required
    def block_user(self, user_id, blocked_user_id):
        response = self._request_put('users/%s/blocks/%s' % (user_id, blocked_user_id))
        return UserBlock.construct_from(response)

    @oauth_required
    def unblock_user(self, user_id, blocked_user_id):
        self._request_delete('users/%s/blocks/%s' % (user_id, blocked_user_id))

    def translate_usernames_to_ids(self, usernames):
        if isinstance(usernames, list):
            usernames = ','.join(usernames)

        response = self._request_get('users?login=%s' % usernames)
        return [User.construct_from(x) for x in response['users']]
