from twitch.conf import credentials_from_config_file
from twitch.constants import (
    PERIODS, PERIOD_ALL, VIDEO_SORTS, VIDEO_SORT_TIME, VIDEO_TYPES, VIDEO_TYPE_ALL
)
from twitch.exceptions import TwitchAttributeException
from twitch.helix.base import APICursor, APIGet
from twitch.resources import Clip, Follow, Game, Stream, StreamMetadata, Video


class TwitchHelix(object):
    """
    Twitch Helix API
    """

    def __init__(self, client_id=None, oauth_token=None):
        self._client_id = client_id
        self._oauth_token = oauth_token

        if not client_id:
            self._client_id, self._oauth_token = credentials_from_config_file()

    def get_streams(self, after=None, before=None, community_ids=None, page_size=20,
                    game_ids=None, languages=None, user_ids=None, user_logins=None):

        if community_ids and len(community_ids) > 100:
            raise TwitchAttributeException('Maximum of 100 Community IDs can be supplied')
        if game_ids and len(game_ids) > 100:
            raise TwitchAttributeException('Maximum of 100 Community IDs can be supplied')
        if languages and len(languages) > 100:
            raise TwitchAttributeException('Maximum of 100 languages can be supplied')
        if user_ids and len(user_ids) > 100:
            raise TwitchAttributeException('Maximum of 100 User IDs can be supplied')
        if user_logins and len(user_logins) > 100:
            raise TwitchAttributeException('Maximum of 100 User login names can be supplied')
        if page_size > 100:
            raise TwitchAttributeException('Maximum number of objects to return is 100')

        params = {
            'after': after,
            'before': before,
            'community_id': community_ids,
            'first': page_size,
            'game_id': game_ids,
            'language': languages,
            'user_id': user_ids,
            'user_login': user_logins,
        }

        return APICursor(
            client_id=self._client_id,
            oauth_token=self._oauth_token,
            path='streams',
            resource=Stream,
            params=params
        )

    def get_games(self, game_ids=None, names=None):
        if game_ids and len(game_ids) > 100:
            raise TwitchAttributeException('Maximum of 100 Game IDs can be supplied')
        if names and len(names) > 100:
            raise TwitchAttributeException('Maximum of 100 Game names can be supplied')

        params = {
            'id': game_ids,
            'name': names,
        }
        return APIGet(
            client_id=self._client_id,
            oauth_token=self._oauth_token,
            path='games',
            resource=Game,
            params=params
        ).fetch()

    def get_clips(self, broadcaster_id=None, game_id=None, clip_ids=None, after=None, before=None,
                  page_size=20):
        if not broadcaster_id and not clip_ids and not game_id:
            raise TwitchAttributeException(
                'At least one of the following parameters must be provided '
                '[broadcaster_id, clip_ids, game_id]'
            )
        if clip_ids and len(clip_ids) > 100:
            raise TwitchAttributeException('Maximum of 100 Clip IDs can be supplied')
        if page_size > 100:
            raise TwitchAttributeException('Maximum number of objects to return is 100')

        params = {
            'broadcaster_id': broadcaster_id,
            'game_id': game_id,
            'id': clip_ids,
            'after': after,
            'before': before,
        }

        if broadcaster_id or game_id:
            params['first'] = page_size

            return APICursor(
                client_id=self._client_id,
                oauth_token=self._oauth_token,
                path='clips',
                resource=Clip,
                params=params
            )

        else:
            return APIGet(
                client_id=self._client_id,
                oauth_token=self._oauth_token,
                path='clips',
                resource=Clip,
                params=params
            ).fetch()

    def get_top_games(self, after=None, before=None, page_size=20):
        if page_size > 100:
            raise TwitchAttributeException('Maximum number of objects to return is 100')

        params = {
            'after': after,
            'before': before,
            'first': page_size,
        }

        return APICursor(
            client_id=self._client_id,
            oauth_token=self._oauth_token,
            path='games/top',
            resource=Game,
            params=params
        )

    def get_videos(self, video_ids=None, user_id=None, game_id=None, after=None, before=None,
                   page_size=20, language=None, period=PERIOD_ALL, sort=VIDEO_SORT_TIME,
                   video_type=VIDEO_TYPE_ALL):
        if video_ids and len(video_ids) > 100:
            raise TwitchAttributeException('Maximum of 100 Video IDs can be supplied')

        params = {
            'id': video_ids,
            'user_id': user_id,
            'game_id': game_id,
        }

        if user_id or game_id:
            if page_size > 100:
                raise TwitchAttributeException('Maximum number of objects to return is 100')
            if period not in PERIODS:
                raise TwitchAttributeException(
                    'Invalid value for period. Valid values are {}'.format(PERIODS)
                )
            if sort not in VIDEO_SORTS:
                raise TwitchAttributeException(
                    'Invalid value for sort. Valid values are {}'.format(VIDEO_SORTS)
                )
            if video_type not in VIDEO_TYPES:
                raise TwitchAttributeException(
                    'Invalid value for video_type. Valid values are {}'.format(VIDEO_TYPES)
                )

            params['after'] = after
            params['before'] = before
            params['first'] = page_size
            params['language'] = language
            params['period'] = period
            params['sort'] = sort
            params['type'] = video_type

            return APICursor(
                client_id=self._client_id,
                oauth_token=self._oauth_token,
                path='videos',
                resource=Video,
                params=params
            )
        else:
            return APIGet(
                client_id=self._client_id,
                oauth_token=self._oauth_token,
                path='videos',
                resource=Video,
                params=params
            ).fetch()

    def get_streams_metadata(self, after=None, before=None, community_ids=None, page_size=20,
                             game_ids=None, languages=None, user_ids=None, user_logins=None):

        if community_ids and len(community_ids) > 100:
            raise TwitchAttributeException('Maximum of 100 Community IDs can be supplied')
        if game_ids and len(game_ids) > 100:
            raise TwitchAttributeException('Maximum of 100 Community IDs can be supplied')
        if languages and len(languages) > 100:
            raise TwitchAttributeException('Maximum of 100 languages can be supplied')
        if user_ids and len(user_ids) > 100:
            raise TwitchAttributeException('Maximum of 100 User IDs can be supplied')
        if user_logins and len(user_logins) > 100:
            raise TwitchAttributeException('Maximum of 100 User login names can be supplied')
        if page_size > 100:
            raise TwitchAttributeException('Maximum number of objects to return is 100')

        params = {
            'after': after,
            'before': before,
            'community_id': community_ids,
            'first': page_size,
            'game_id': game_ids,
            'language': languages,
            'user_id': user_ids,
            'user_login': user_logins,
        }

        return APICursor(
            client_id=self._client_id,
            oauth_token=self._oauth_token,
            path='streams/metadata',
            resource=StreamMetadata,
            params=params
        )

    def get_user_follows(self, after=None, page_size=20, from_id=None, to_id=None):
        if not from_id and not to_id:
            raise TwitchAttributeException('from_id or to_id must be provided.')
        if page_size > 100:
            raise TwitchAttributeException('Maximum number of objects to return is 100')

        params = {
            'after': after,
            'first': page_size,
            'from_id': from_id,
            'to_id': to_id,
        }

        return APICursor(
            client_id=self._client_id,
            oauth_token=self._oauth_token,
            path='users/follows',
            resource=Follow,
            params=params
        )
