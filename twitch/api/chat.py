from twitch.api.base import TwitchAPI


class Chat(TwitchAPI):

    def get_badges_by_channel(self, channel_id):
        response = self._request_get('chat/%s/badges' % channel_id)
        return response

    def get_emoticons_by_set(self, emotesets=None):
        params = {
            'emotesets': emotesets,
        }
        response = self._request_get('chat/emoticon_images', params=params)
        return response

    def get_all_emoticons(self):
        response = self._request_get('chat/emoticons')
        return response
