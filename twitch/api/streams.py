from twitch.api.base import TwitchAPI
from twitch.constants import STREAM_TYPE_LIVE, STREAM_TYPES
from twitch.decorators import oauth_required
from twitch.exceptions import TwitchAttributeException
from twitch.resources import Featured, Stream


class Streams(TwitchAPI):
    async def get_stream_by_user(self, channel_id, stream_type=STREAM_TYPE_LIVE):
        if stream_type not in STREAM_TYPES:
            raise TwitchAttributeException(
                "Stream type is not valid. Valid values are {}".format(STREAM_TYPES)
            )

        params = {
            "stream_type": stream_type,
        }
        response = await self._request_get("streams/{}".format(channel_id), params=params)

        if not response["stream"]:
            return None
        return Stream.construct_from(response["stream"])

    async def get_live_streams(
        self,
        channel=None,
        game=None,
        language=None,
        stream_type=STREAM_TYPE_LIVE,
        limit=25,
        offset=0,
    ):
        if limit > 100:
            raise TwitchAttributeException(
                "Maximum number of objects returned in one request is 100"
            )

        params = {"stream_type": stream_type, "limit": limit, "offset": offset}
        if channel is not None:
            params["channel"] = channel
        if game is not None:
            params["game"] = game
        if language is not None:
            params["language"] = language
        response = await self._request_get("streams", params=params)
        return [Stream.construct_from(x) for x in response["streams"]]

    async def get_summary(self, game=None):
        params = {}
        if game is not None:
            params["game"] = game
        response = await self._request_get("streams/summary", params=params)
        return response

    async def get_featured(self, limit=25, offset=0):
        if limit > 100:
            raise TwitchAttributeException(
                "Maximum number of objects returned in one request is 100"
            )

        params = {"limit": limit, "offset": offset}
        response = await self._request_get("streams/featured", params=params)
        return [Featured.construct_from(x) for x in response["featured"]]

    @oauth_required
    async def get_followed(self, stream_type=STREAM_TYPE_LIVE, limit=25, offset=0):
        if stream_type not in STREAM_TYPES:
            raise TwitchAttributeException(
                "Stream type is not valid. Valid values are {}".format(STREAM_TYPES)
            )
        if limit > 100:
            raise TwitchAttributeException(
                "Maximum number of objects returned in one request is 100"
            )

        params = {"stream_type": stream_type, "limit": limit, "offset": offset}
        response = await self._request_get("streams/followed", params=params)
        return [Stream.construct_from(x) for x in response["streams"]]

    async def get_streams_in_community(self, community_id):
        response = await self._request_get("streams?community_id={}".format(community_id))

        return [Stream.construct_from(x) for x in response["streams"]]
