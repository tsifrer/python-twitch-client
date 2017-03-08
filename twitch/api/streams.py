from twitch.api.base import TwitchAPI
from twitch.constants import STREAM_TYPES, STREAM_TYPE_LIVE
from twitch.decorators import oauth_required
from twitch.exceptions import TwitchAttributeException
from twitch.resources import Featured, Stream


class Streams(TwitchAPI):

    def get_stream_by_user(self, channel_id, stream_type=STREAM_TYPE_LIVE):
        if stream_type not in STREAM_TYPES:
            raise TwitchAttributeException(
                'Stream type is not valid. Valid values are %s' % STREAM_TYPES)

        params = {
            'stream_type': stream_type,
        }
        response = self._request_get('streams/%s' % channel_id, params=params)
        return Stream.construct_from(response['stream'])

    def get_live_streams(self, channel=None, game=None, language=None, stream_type=STREAM_TYPE_LIVE,
                         limit=25, offset=0):
        if limit > 100:
            raise TwitchAttributeException(
                'Maximum number of objects returned in one request is 100')

        params = {
            'stream_type': stream_type,
            'limit': limit,
            'offset': offset
        }
        if channel is not None:
            params['channel'] = channel
        if game is not None:
            params['game'] = game
        if language is not None:
            params['language'] = language
        response = self._request_get('streams', params=params)
        return [Stream.construct_from(x) for x in response['streams']]

    def get_summary(self, game=None):
        params = {}
        if game is not None:
            params['game'] = game
        response = self._request_get('streams/summary', params=params)
        return response

    def get_featured(self, limit=25, offset=0):
        if limit > 100:
            raise TwitchAttributeException(
                'Maximum number of objects returned in one request is 100')

        params = {
            'limit': limit,
            'offset': offset
        }
        response = self._request_get('streams/featured', params=params)
        return [Featured.construct_from(x) for x in response['featured']]

    @oauth_required
    def get_followed(self, stream_type=STREAM_TYPE_LIVE, limit=25, offset=0):
        if stream_type not in STREAM_TYPES:
            raise TwitchAttributeException(
                'Stream type is not valid. Valid values are %s' % STREAM_TYPES)
        if limit > 100:
            raise TwitchAttributeException(
                'Maximum number of objects returned in one request is 100')

        params = {
            'stream_type': stream_type,
            'limit': limit,
            'offset': offset
        }
        response = self._request_get('streams/followed', params=params)
        return [Stream.construct_from(x) for x in response['streams']]
