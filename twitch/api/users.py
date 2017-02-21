from twitch.api.base import TwitchAPI
from twitch.constants import DIRECTIONS, DIRECTION_DESC, USERS_SORT_BY, USERS_SORT_BY_CREATED_AT
from twitch.resources import Follow, Subscription, User, UserBlock


class Users(TwitchAPI):

    def get(self):
        response = self._request_get('user')
        return User.construct_from(response)

    def get_by_id(self, user_id):
        # https://dev.twitch.tv/docs/v5/reference/users/#get-user-by-id
        url = 'users/%s' % (user_id)

        response = self._request_get(url)
        return User.construct_from(response)

    def get_emotes(self, user_id):
        # https://dev.twitch.tv/docs/v5/reference/users/#get-user-emotes
        url = 'users/%s/emotes' % (user_id)

        response = self._request_get(url)
        return response['emoticon_sets']

    def check_subscribed_to_channel(self, user_id, channel_id):
        # https://dev.twitch.tv/docs/v5/reference/users/#check-user-subscription-by-channel
        url = 'users/%s/subscriptions/%s' % (user_id, channel_id)

        response = self._request_get(url)
        return Subscription.construct_from(response)

    def get_follows(self, user_id, limit=25, offset=0, direction=DIRECTION_DESC,
                    sort_by=USERS_SORT_BY_CREATED_AT):
        # https://dev.twitch.tv/docs/v5/reference/users/#get-user-follows
        assert limit <= 100, 'Maximum number of videos returned in one request is 100'
        assert direction in DIRECTIONS, 'Direction is not valid. Valid values are %s' % DIRECTIONS
        assert sort_by in USERS_SORT_BY, 'Sort by is not valud. Valid values are %s' % USERS_SORT_BY

        url = 'users/%s/follows/channels' % user_id

        params = {
            'limit': limit,
            'offset': offset,
            'direction': direction
        }
        response = self._request_get(url, params=params)
        return [Follow.construct_from(x) for x in response['follows']]

    def check_follows_channel(self, user_id, channel_id):
        # https://dev.twitch.tv/docs/v5/reference/users/#check-user-follows-by-channel
        url = 'users/%s/follows/channels/%s' % (user_id, channel_id)

        response = self._request_get(url)
        return Follow.construct_from(response)

    def follow_channel(self, user_id, channel_id, notifications=False):
        # https://dev.twitch.tv/docs/v5/reference/users/#follow-channel
        url = 'users/%s/follows/channels/%s' % (user_id, channel_id)
        data = {
            'notifications': notifications
        }
        response = self._request_put(url, data)
        return Follow.construct_from(response)

    def unfollow_channel(self, user_id, channel_id):
        # https://dev.twitch.tv/docs/v5/reference/users/#unfollow-channel
        url = 'users/%s/follows/channels/%s' % (user_id, channel_id)
        # TODO: properly handle response
        self._request_delete(url)

    def get_user_block_list(self, user_id, limit=25, offset=0):
        # https://dev.twitch.tv/docs/v5/reference/users/#get-user-block-list
        assert limit <= 100, 'Maximum number of videos returned in one request is 100'

        url = 'users/%s/blocks' % user_id
        params = {
            'limit': limit,
            'offset': offset
        }
        response = self._request_get(url, params=params)
        return [UserBlock.construct_from(x) for x in response['blocks']]

    def block_user(self, user_id, blocked_user_id):
        # https://dev.twitch.tv/docs/v5/reference/users/#block-user
        url = 'users/%s/blocks/%s' % (user_id, blocked_user_id)
        response = self._request_put(url)
        return UserBlock.construct_from(response)

    def unblock_user(self, user_id, blocked_user_id):
        # https://dev.twitch.tv/docs/v5/reference/users/#unblock-user
        url = 'users/%s/blocks/%s' % (user_id, blocked_user_id)
        # TODO: properly handle response
        self._request_delete(url)

    def translate_usernames_to_ids(self, usernames):
        if isinstance(usernames, list):
            usernames = ','.join(usernames)

        url = 'users?login=%s' % usernames
        response = self._request_get(url)
        return [User.construct_from(x) for x in response['users']]
