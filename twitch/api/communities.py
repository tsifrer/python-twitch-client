from twitch.api.base import TwitchAPI
from twitch.decorators import oauth_required
from twitch.exceptions import TwitchAttributeException
from twitch.resources import Community, User


class Communities(TwitchAPI):

    def get_by_name(self, community_name):
        params = {
            'name': community_name
        }
        response = self._request_get('communities', params=params)
        return Community.construct_from(response)

    def get_by_id(self, community_id):
        response = self._request_get('communities/%s' % community_id)
        return Community.construct_from(response)

    def update(self, community_id, summary=None, description=None, rules=None, email=None):
        data = {
            'summary': summary,
            'description': description,
            'rules': rules,
            'email': email
        }
        self._request_put('communities/%s' % community_id, data=data)

    def get_top(self, limit=10, cursor=None):
        if limit > 100:
            raise TwitchAttributeException(
                'Maximum number of objects returned in one request is 100')
        params = {
            'limit': limit,
            'cursor': cursor
        }
        response = self._request_get('communities/top', params=params)
        return [Community.construct_from(x) for x in response['communities']]

    @oauth_required
    def get_banned_users(self, community_id, limit=10, cursor=None):
        if limit > 100:
            raise TwitchAttributeException(
                'Maximum number of objects returned in one request is 100')

        params = {
            'limit': limit,
            'cursor': cursor
        }
        response = self._request_get('communities/%s/bans' % community_id, params=params)
        return [User.construct_from(x) for x in response['banned_users']]

    @oauth_required
    def ban_user(self, community_id, user_id):
        self._request_put('communities/%s/bans/%s' % (community_id, user_id))

    @oauth_required
    def unban_user(self, community_id, user_id):
        self._request_delete('communities/%s/bans/%s' % (community_id, user_id))

    @oauth_required
    def create_avatar_image(self, community_id, avatar_image):
        data = {
            'avatar_image': avatar_image,
        }
        self._request_post('communities/%s/images/avatar' % community_id, data=data)

    @oauth_required
    def delete_avatar_image(self, community_id):
        self._request_delete('communities/%s/images/avatar' % community_id)

    @oauth_required
    def create_cover_image(self, community_id, cover_image):
        data = {
            'cover_image': cover_image,
        }
        self._request_post('communities/%s/images/cover' % community_id, data=data)

    @oauth_required
    def delete_cover_image(self, community_id):
        self._request_delete('communities/%s/images/cover' % community_id)

    def get_moderators(self, community_id):
        response = self._request_get('communities/%s/moderators' % community_id)
        return [User.construct_from(x) for x in response['moderators']]

    @oauth_required
    def add_moderator(self, community_id, user_id):
        self._request_put('communities/%s/moderators/%s' % (community_id, user_id))

    @oauth_required
    def delete_moderator(self, community_id, user_id):
        self._request_delete('communities/%s/moderators/%s' % (community_id, user_id))

    @oauth_required
    def get_permissions(self, community_id):
        response = self._request_get('communities/%s/permissions' % community_id)
        return response

    @oauth_required
    def report_violation(self, community_id, channel_id):
        data = {
            'channel_id': channel_id,
        }
        self._request_post('communities/%s/report_channel' % community_id, data=data)

    @oauth_required
    def get_timed_out_users(self, community_id, limit=10, cursor=None):
        if limit > 100:
            raise TwitchAttributeException(
                'Maximum number of objects returned in one request is 100')
        params = {
            'limit': limit,
            'cursor': cursor
        }
        response = self._request_get('communities/%s/timeouts' % community_id, params=params)
        return [User.construct_from(x) for x in response['timed_out_users']]

    @oauth_required
    def add_timed_out_user(self, community_id, user_id, duration, reason=None):
        data = {
            'duration': duration,
            'reason': reason,
        }
        self._request_put('communities/%s/timeouts/%s' % (community_id, user_id), data=data)

    @oauth_required
    def delete_timed_out_user(self, community_id, user_id):
        self._request_delete('communities/%s/timeouts/%s' % (community_id, user_id))
