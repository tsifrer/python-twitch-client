import time

import requests
from requests import codes
from requests.compat import urljoin

from twitch.constants import BASE_HELIX_URL
from twitch.exceptions import TwitchNotProvidedException


class TwitchAPIMixin(object):
    _rate_limit_resets = set()
    _rate_limit_remaining = 0

    def _wait_for_rate_limit_reset(self):
        if self._rate_limit_remaining == 0:
            current_time = int(time.time())
            self._rate_limit_resets = set(x for x in self._rate_limit_resets if x > current_time)

            if len(self._rate_limit_resets) > 0:
                reset_time = list(self._rate_limit_resets)[0]

                # Calculate wait time and add 0.1s to the wait time to allow Twitch to reset
                # their counter
                wait_time = reset_time - current_time + 0.1
                time.sleep(wait_time)

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

        self._wait_for_rate_limit_reset()

        response = requests.get(url, params=params, headers=headers)

        remaining = response.headers.get('Ratelimit-Remaining')
        if remaining:
            self._rate_limit_remaining = int(remaining)

        reset = response.headers.get('Ratelimit-Reset')
        if reset:
            self._rate_limit_resets.add(int(reset))

        # If status code is 429, re-run _request_get which will wait for the appropriate time
        # to obey the rate limit
        if response.status_code == codes.TOO_MANY_REQUESTS:
            return self._request_get(path, params=params)

        response.raise_for_status()
        return response.json()


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
        self._total = None

        # Pre-fetch the first page as soon as cursor is instantiated
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
        if self._cursor:
            self._params['after'] = self._cursor

        response = self._request_get(self._path, params=self._params)

        self._queue = [self._resource.construct_from(data) for data in response['data']]
        self._cursor = response['pagination'].get('cursor')
        self._total = response.get('total')
        return self._queue

    @property
    def cursor(self):
        return self._cursor

    @property
    def total(self):
        if not self._total:
            raise TwitchNotProvidedException()
        return self._total


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
