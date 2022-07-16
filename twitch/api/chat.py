from twitch.api.base import TwitchAPI


class Chat(TwitchAPI):
    async def get_badges_by_channel(self, channel_id):
        response = await self._request_get("chat/{}/badges".format(channel_id))
        return response

    async def get_emoticons_by_set(self, emotesets=None):
        params = {
            "emotesets": emotesets,
        }
        response = await self._request_get("chat/emoticon_images", params=params)
        return response

    async def get_all_emoticons(self):
        response = await self._request_get("chat/emoticons")
        return response
