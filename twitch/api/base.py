import requests
from requests.compat import urljoin


BASE_URL = 'https://api.twitch.tv/kraken/'


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
        # TODO: error handling
        response = requests.get(url, params=params, headers=headers)
        return response.json()

    def _request_put(self, path, data=None):
        url = urljoin(BASE_URL, path)

        headers = self._get_request_headers()
        # TODO: error handling
        response = requests.put(url, data=data, headers=headers)
        return response.json()

    def _request_delete(self, path):
        url = urljoin(BASE_URL, path)
        headers = self._get_request_headers()
        # TODO: error handling and response handling
        requests.put(url, headers=headers)
