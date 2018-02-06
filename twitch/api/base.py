import os
import time
from configparser import ConfigParser

import requests
from requests.compat import urljoin

from twitch.constants import BASE_URL, CONFIG_FILE_PATH


class TwitchAPI(object):

    def __init__(self, client_id, oauth_token=None, *args, **kwargs):
        super(TwitchAPI, self).__init__()
        self._client_id = client_id
        self._oauth_token = oauth_token
        self._initial_backoff = None
        self._max_retries = None
        self._read_backoff_configuration_from_file()

    def _read_backoff_configuration_from_file(self):
        config = ConfigParser()
        config.read(os.path.expanduser(CONFIG_FILE_PATH))

        if 'General' in config.sections():
            self._initial_backoff = float(config['General']['initial_backoff'])
            self._max_retries = int(config['General']['max_retries'])
        else:
            self._initial_backoff = 0.5
            self._max_retries = 3

    def _get_request_headers(self):
        headers = {
            'Accept': 'application/vnd.twitchtv.v5+json',
            'Client-ID': self._client_id
        }

        if self._oauth_token:
            headers['Authorization'] = 'OAuth %s' % self._oauth_token

        return headers

    def _request_get(self, path, params=None, json=True, url=BASE_URL):
        url = urljoin(url, path)
        headers = self._get_request_headers()

        response = requests.get(url, params=params, headers=headers)
        if response.status_code >= 500:

            backoff = self._initial_backoff
            for _ in range(self._max_retries):
                time.sleep(backoff)
                backoff_response = requests.get(url, params=params, headers=headers)
                if backoff_response.status_code < 500:
                    response = backoff_response
                    break
                backoff *= 2

        response.raise_for_status()
        if json:
            return response.json()
        else:
            return response

    def _request_post(self, path, data=None, params=None, url=BASE_URL):
        url = urljoin(url, path)

        headers = self._get_request_headers()

        response = requests.post(url, json=data, params=params, headers=headers)
        response.raise_for_status()
        if response.status_code == 200:
            return response.json()

    def _request_put(self, path, data=None, params=None, url=BASE_URL):
        url = urljoin(url, path)

        headers = self._get_request_headers()
        response = requests.put(url, json=data, params=params, headers=headers)
        response.raise_for_status()
        if response.status_code == 200:
            return response.json()

    def _request_delete(self, path, params=None, url=BASE_URL):
        url = urljoin(url, path)

        headers = self._get_request_headers()

        response = requests.delete(url, params=params, headers=headers)
        response.raise_for_status()
        if response.status_code == 200:
            return response.json()
