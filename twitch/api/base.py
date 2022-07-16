import time

# import requests
# from requests.compat import urljoin
import aiohttp

from twitch.conf import backoff_config
from twitch.constants import BASE_URL

DEFAULT_TIMEOUT = 10


class TwitchAPI(object):
    """Twitch API client."""

    def __init__(self, client_id, oauth_token=None):
        """Initialize the API."""
        super(TwitchAPI, self).__init__()
        self._client_id = client_id
        self._oauth_token = oauth_token
        self._initial_backoff, self._max_retries = backoff_config()

    def _get_request_headers(self):
        """Prepare the headers for the requests."""
        headers = {
            "Accept": "application/vnd.twitchtv.v5+json",
            "Client-ID": self._client_id,
        }

        if self._oauth_token:
            headers["Authorization"] = "OAuth {}".format(self._oauth_token)

        return headers

    async def _request_get(self, path, params=None, json=True, url=BASE_URL):
        """Perform a HTTP GET request."""
        url = f"{url}{path}"
        headers = self._get_request_headers()

        async with aiohttp.ClientSession(raise_for_status=True) as session:
            async with session.request("GET", url, params=params, headers=headers) as response:
                if response.status >= 500:

                    backoff = self._initial_backoff
                    for _ in range(self._max_retries):
                        time.sleep(backoff)
                        async with session.request("GET", url, params=params, headers=headers, timeout=DEFAULT_TIMEOUT) as backoff_response:
                            if backoff_response.status < 500:
                                response = backoff_response
                                break
                            backoff *= 2

                if json:
                    return await response.json()
                else:
                    return response

    async def _request_post(self, path, data=None, params=None, url=BASE_URL):
        """Perform a HTTP POST request.."""
        url = f"{url}{path}"

        headers = self._get_request_headers()

        async with aiohttp.ClientSession() as session:
            async with session.request("POST", url, data=data, params=params, headers=headers, raise_for_status=True) as response:
                if response.status == 200:
                    return await response.json()

    async def _request_put(self, path, data=None, params=None, url=BASE_URL):
        """Perform a HTTP PUT request."""
        url = f"{url}{path}"

        headers = self._get_request_headers()
        async with aiohttp.ClientSession() as session:
            async with session.request("PUT", url, data=data, params=params, headers=headers, raise_for_status=True) as response:
                if response.status == 200:
                    return await response.json()

    async def _request_delete(self, path, params=None, url=BASE_URL):
        """Perform a HTTP DELETE request."""
        url = f"{url}{path}"

        headers = self._get_request_headers()
        async with aiohttp.ClientSession() as session:
            async with session.request("DELETE", url, params=params, headers=headers, raise_for_status=True) as response:
                if response.status == 200:
                    return await response.json()
