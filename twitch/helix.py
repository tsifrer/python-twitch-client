import time

import requests
from requests.compat import urljoin

from .api.base import get_credentials_from_cfg_file
from .constants import BASE_HELIX_URL
from .resources import Clip, Game, Stream


class TwitchAPIMixin(object):

    def _get_request_headers(self):
        headers = {
            'Client-ID': self._client_id
        }

        if self._oauth_token:
            headers['Authorization'] = 'Bearer %s' % self._oauth_token

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

    def __init__(self, client_id, path, resource, oauth_token=None, cursor=None):
        super(APICursor, self).__init__()
        self._path = path
        self._queue = []
        self._cursor = cursor
        self._resource = resource
        self._client_id = client_id
        self._oauth_token = oauth_token

        self.next_page()

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
        params = {
            'first': 100
        }
        if self._cursor:
            params['after'] = self._cursor

        print(params)

        time.sleep(1)
        response = self._request_get(self._path, params=params)

        self._queue = [self._resource.construct_from(data) for data in response['data']]
        self._cursor = response['pagination'].get('cursor')
        print(response['pagination'])
        return self._queue


class TwitchHelix(object):
    """
    New Twitch API [helix]
    """

    def __init__(self, client_id=None, oauth_token=None):
        self._client_id = client_id
        self._oauth_token = oauth_token

        if not client_id:
            self._client_id, self._oauth_token = get_credentials_from_cfg_file()

    def get_streams(self):
        return APICursor(
            client_id=self._client_id,
            oauth_token=self._oauth_token,
            path='streams',
            resource=Stream
        )

    def get_games(self, game_ids=None, names=None):
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

    def get_clip(self, clip_id):
        params = {
            'id': clip_id
        }
        clips = APIGet(
            client_id=self._client_id,
            oauth_token=self._oauth_token,
            path='clips',
            resource=Clip,
            params=params
        ).fetch()

        if len(clips) == 1:
            return clips[0]
        else:
            return None
