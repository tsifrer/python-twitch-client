import time

import requests
from requests.compat import urljoin

from twitch.api.base import get_credentials_from_cfg_file
from twitch.constants import BASE_HELIX_URL
from twitch.exceptions import TwitchAttributeException
from twitch.resources import Clip, Game, Stream, Video


class TwitchAPIMixin(object):

    def _get_request_headers(self):
        headers = {
            'Client-ID': self._client_id
        }

        if self._oauth_token:
            headers['Authorization'] = 'Bearer {}'.format(self._oauth_token)

        return headers

    def _request_get(self, path, params=None):
        url = urljoin(BASE_HELIX_URL, path)

        headers = self._get_request_headers()

        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        return response.json()


class APIGet(TwitchAPIMixin):

    def __init__(self, client_id, path, resource, oauth_token=None, params=None):
        super(APIGet, self).__init__()
        self._path = path
        self._resource = resource
        self._client_id = client_id
        self._oauth_token = oauth_token
        self._params = params

    def fetch(self):
        response = self._request_get(self._path, params=self._params)
        return [self._resource.construct_from(data) for data in response['data']]


class APICursor(TwitchAPIMixin):

    def __init__(self, client_id, path, resource, oauth_token=None, cursor=None, params=None):
        super(APICursor, self).__init__()
        self._path = path
        self._queue = []
        self._cursor = cursor
        self._resource = resource
        self._client_id = client_id
        self._oauth_token = oauth_token
        self._params = params

    def __repr__(self):
        return str(self._queue)

    def __len__(self):
        return len(self._queue)

    def __iter__(self):
        return self

    def __next__(self):
        if not self._queue and not self.next_page():
            raise StopIteration()

        return self._queue.pop(0)

    # Python 2 compatibility.
    next = __next__

    def __getitem__(self, index):
        return self._queue[index]

    def next_page(self):
        if self._cursor:
            self._params['after'] = self._cursor

         # TODO: fix sleep to obey rate limit rules and ignore it in tests
        time.sleep(1)
        response = self._request_get(self._path, params=self._params)

        self._queue = [self._resource.construct_from(data) for data in response['data']]
        self._cursor = response['pagination'].get('cursor')
        return self._queue


class TwitchHelix(object):
    """
    Twitch Helix API
    """

    def __init__(self, client_id=None, oauth_token=None):
        self._client_id = client_id
        self._oauth_token = oauth_token

        if not client_id:
            self._client_id, self._oauth_token = get_credentials_from_cfg_file()

     # Tested
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

     # Tested
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

     # Tested
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

     # Tested
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
                   page_size=None, language=None, period=None, sort=None, video_type=None):
        if video_ids and len(video_ids) > 100:
            raise TwitchAttributeException('Maximum of 100 Video IDs can be supplied')
        params = {
            'id': video_ids,
            'user_id': user_id,
            'game_id': game_id,
            'after': after,
            'before': before,
            'first': page_size,
            'language': language,
            'period': period,
            'sort': sort,
            'type': video_type
        }

        return APICursor(
            client_id=self._client_id,
            oauth_token=self._oauth_token,
            path='videos',
            resource=Video,
            params=params
        )
