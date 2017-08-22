import json
import os

import pytest

from requests import exceptions

import responses

from twitch.api.base import BASE_URL, TwitchAPI


dummy_data = {
    'spongebob': 'squarepants'
}


def test_get_request_headers_include_version_and_client_id():
    client_id = 'abcd'
    api = TwitchAPI(client_id=client_id)

    headers = api._get_request_headers()

    assert len(headers) == 2
    assert headers['Accept'] == 'application/vnd.twitchtv.v5+json'
    assert headers['Client-ID'] == client_id


def test_get_request_headers_includes_authorization():
    client_id = 'client'
    oauth_token = 'token'
    api = TwitchAPI(client_id=client_id, oauth_token=oauth_token)

    headers = api._get_request_headers()

    assert len(headers) == 3
    assert headers['Accept'] == 'application/vnd.twitchtv.v5+json'
    assert headers['Client-ID'] == client_id
    assert headers['Authorization'] == 'OAuth %s' % oauth_token


@responses.activate
def test_request_get_returns_dictionary_if_successful():
    responses.add(responses.GET,
                  BASE_URL,
                  body=json.dumps(dummy_data),
                  status=200,
                  content_type='application/json')

    api = TwitchAPI(client_id='client')
    response = api._request_get('')

    assert isinstance(response, dict)
    assert response == dummy_data


@responses.activate
def test_request_get_sends_headers_with_the_request():
    responses.add(responses.GET,
                  BASE_URL,
                  body=json.dumps(dummy_data),
                  status=200,
                  content_type='application/json')

    api = TwitchAPI(client_id='client')
    api._request_get('')

    assert 'Client-ID' in responses.calls[0].request.headers
    assert 'Accept' in responses.calls[0].request.headers


@responses.activate
@pytest.mark.parametrize('status', [
    (500),
    (400),
])
def test_request_get_raises_exception_if_not_200_response(status, monkeypatch):
    responses.add(responses.GET,
                  BASE_URL,
                  status=status,
                  content_type='application/json')

    def mockreturn(path):
        return 'tests/api/dummy_credentials.cfg'

    monkeypatch.setattr(os.path, 'expanduser', mockreturn)

    api = TwitchAPI(client_id='client')

    with pytest.raises(exceptions.HTTPError):
        api._request_get('')


@responses.activate
def test_request_put_returns_dictionary_if_successful():
    responses.add(responses.PUT,
                  BASE_URL,
                  body=json.dumps(dummy_data),
                  status=200,
                  content_type='application/json')

    api = TwitchAPI(client_id='client')
    response = api._request_put('', dummy_data)

    assert isinstance(response, dict)
    assert response == dummy_data


@responses.activate
def test_request_put_sends_headers_with_the_request():
    responses.add(responses.PUT,
                  BASE_URL,
                  status=204,
                  content_type='application/json')

    api = TwitchAPI(client_id='client')
    api._request_put('', dummy_data)

    assert 'Client-ID' in responses.calls[0].request.headers
    assert 'Accept' in responses.calls[0].request.headers


@responses.activate
def test_request_put_does_not_raise_exception_if_successful_and_returns_json():
    responses.add(responses.PUT,
                  BASE_URL,
                  body=json.dumps(dummy_data),
                  status=200,
                  content_type='application/json')

    api = TwitchAPI(client_id='client')
    response = api._request_put('', dummy_data)
    assert response == dummy_data


@responses.activate
@pytest.mark.parametrize('status', [
    (500),
    (400),
])
def test_request_put_raises_exception_if_not_200_response(status):
    responses.add(responses.PUT,
                  BASE_URL,
                  status=status,
                  content_type='application/json')

    api = TwitchAPI(client_id='client')

    with pytest.raises(exceptions.HTTPError):
        api._request_put('', dummy_data)


@responses.activate
def test_request_delete_does_not_raise_exception_if_successful():
    responses.add(responses.DELETE,
                  BASE_URL,
                  status=204,
                  content_type='application/json')

    api = TwitchAPI(client_id='client')
    api._request_delete('')


@responses.activate
def test_request_delete_does_not_raise_exception_if_successful_and_returns_json():
    responses.add(responses.DELETE,
                  BASE_URL,
                  body=json.dumps(dummy_data),
                  status=200,
                  content_type='application/json')

    api = TwitchAPI(client_id='client')
    response = api._request_delete('')
    assert response == dummy_data


@responses.activate
def test_request_delete_sends_headers_with_the_request():
    responses.add(responses.DELETE,
                  BASE_URL,
                  status=204,
                  content_type='application/json')

    api = TwitchAPI(client_id='client')
    api._request_delete('')

    assert 'Client-ID' in responses.calls[0].request.headers
    assert 'Accept' in responses.calls[0].request.headers


@responses.activate
@pytest.mark.parametrize('status', [
    (500),
    (400),
])
def test_request_delete_raises_exception_if_not_200_response(status):
    responses.add(responses.DELETE,
                  BASE_URL,
                  status=status,
                  content_type='application/json')

    api = TwitchAPI(client_id='client')

    with pytest.raises(exceptions.HTTPError):
        api._request_delete('')


@responses.activate
def test_request_post_returns_dictionary_if_successful():
    responses.add(responses.POST,
                  BASE_URL,
                  body=json.dumps(dummy_data),
                  status=200,
                  content_type='application/json')

    api = TwitchAPI(client_id='client')
    response = api._request_post('', dummy_data)

    assert isinstance(response, dict)
    assert response == dummy_data


@responses.activate
def test_request_post_does_not_raise_exception_if_successful():
    responses.add(responses.POST,
                  BASE_URL,
                  status=204,
                  content_type='application/json')

    api = TwitchAPI(client_id='client')
    api._request_post('')


@responses.activate
def test_request_post_sends_headers_with_the_request():
    responses.add(responses.POST,
                  BASE_URL,
                  body=json.dumps(dummy_data),
                  status=200,
                  content_type='application/json')

    api = TwitchAPI(client_id='client')
    api._request_post('', dummy_data)

    assert 'Client-ID' in responses.calls[0].request.headers
    assert 'Accept' in responses.calls[0].request.headers


@responses.activate
@pytest.mark.parametrize('status', [
    (500),
    (400),
])
def test_request_post_raises_exception_if_not_200_response(status):
    responses.add(responses.POST,
                  BASE_URL,
                  status=status,
                  content_type='application/json')

    api = TwitchAPI(client_id='client')

    with pytest.raises(exceptions.HTTPError):
        api._request_post('', dummy_data)
