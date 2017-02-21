from twitch.api.base import TwitchAPI
from twitch.resources import Community


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

    def create(self, name, summary=None, description=None, rules=None):
        data = {
            'name': name,
            'summary': summary,
            'description': description,
            'rules': rules
        }
        response = self._request_post('communities', data=data)
        return Community.construct_from(response)

    def update(self, community_id, summary=None, description=None, rules=None, email=None):
        data = {
            'summary': summary,
            'description': description,
            'rules': rules,
            'email': email
        }
        self._request_put('communities/%s' % community_id, data=data)
