import requests
from requests.compat import urljoin

from twitch.constants import BASE_URL


class TwitchAPI(object):

    def __init__(self, client_id, oauth_token=None, *args, **kwargs):
        super(TwitchAPI, self).__init__()
        self._client_id = client_id
        self._oauth_token = oauth_token

    def _get_request_headers(self):
        headers = {
            'Accept': 'application/vnd.twitchtv.v5+json',
            'Client-ID': self._client_id
        }

        if self._oauth_token:
            headers['Authorization'] = 'OAuth %s' % self._oauth_token

        return headers

    def _request_get(self, path, params=None):
        url = urljoin(BASE_URL, path)

        headers = self._get_request_headers()

        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        return response.json()

    def _request_post(self, path, data=None, params=None):
        url = urljoin(BASE_URL, path)

        headers = self._get_request_headers()

        response = requests.post(url, data=data, params=params, headers=headers)
        response.raise_for_status()
        if response.status_code == 200:
            return response.json()

    def _request_put(self, path, data=None, params=None):
        url = urljoin(BASE_URL, path)

        headers = self._get_request_headers()

        response = requests.put(url, data=data, params=params, headers=headers)
        response.raise_for_status()
        if response.status_code == 200:
            return response.json()

    def _request_delete(self, path, params=None):
        url = urljoin(BASE_URL, path)

        headers = self._get_request_headers()

        response = requests.delete(url, params=params, headers=headers)
        response.raise_for_status()
        if response.status_code == 200:
            return response.json()
