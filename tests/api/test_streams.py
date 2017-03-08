import json

import pytest

import responses

from twitch.client import TwitchClient
from twitch.constants import BASE_URL
from twitch.exceptions import TwitchException
from twitch.resources import Channel, Featured, Stream

example_stream = {
    '_id': 23932774784,
    'game': 'BATMAN - The Telltale Series',
    'channel': {
        '_id': 7236692,
        'name': 'dansgaming',
    }
}

example_stream_response = {
    'stream': example_stream
}

example_streams_response = {
   '_total': 1295,
   'streams': [example_stream]
}

example_featured_response = {
   'featured': [{
        'title': 'Bethesda Plays The Elder Scrolls: Legends | More Arena & Deckbuilding',
        'stream': example_stream
    }]
}


@responses.activate
def test_get_stream_by_user():
    channel_id = 7236692
    responses.add(responses.GET,
                  '%sstreams/%s' % (BASE_URL, channel_id),
                  body=json.dumps(example_stream_response),
                  status=200,
                  content_type='application/json')

    client = TwitchClient('client id')

    stream = client.streams.get_stream_by_user(channel_id)

    assert len(responses.calls) == 1
    assert isinstance(stream, Stream)
    assert stream.id == example_stream_response['stream']['_id']
    assert stream.game == example_stream_response['stream']['game']

    assert isinstance(stream.channel, Channel)
    assert stream.channel.id == example_stream_response['stream']['channel']['_id']
    assert stream.channel.name == example_stream_response['stream']['channel']['name']


@responses.activate
@pytest.mark.parametrize('param,value', [
    ('stream_type', 'abcd'),
])
def test_get_stream_by_user_raises_if_wrong_params_are_passed_in(param, value):
    client = TwitchClient('client id')
    kwargs = {param: value}
    with pytest.raises(TwitchException):
        client.streams.get_stream_by_user('1234', **kwargs)


@responses.activate
def test_get_live_streams():
    responses.add(responses.GET,
                  '%sstreams' % BASE_URL,
                  body=json.dumps(example_streams_response),
                  status=200,
                  content_type='application/json')

    client = TwitchClient('client id')

    streams = client.streams.get_live_streams()

    assert len(responses.calls) == 1
    assert len(streams) == 1
    stream = streams[0]
    assert isinstance(stream, Stream)
    assert stream.id == example_stream_response['stream']['_id']
    assert stream.game == example_stream_response['stream']['game']

    assert isinstance(stream.channel, Channel)
    assert stream.channel.id == example_stream_response['stream']['channel']['_id']
    assert stream.channel.name == example_stream_response['stream']['channel']['name']


@responses.activate
@pytest.mark.parametrize('param,value', [
    ('limit', 101),
])
def test_get_live_streams_raises_if_wrong_params_are_passed_in(param, value):
    client = TwitchClient('client id')
    kwargs = {param: value}
    with pytest.raises(TwitchException):
        client.streams.get_live_streams(**kwargs)


@responses.activate
def test_get_summary():
    response = {
        'channels': 1417,
        'viewers': 19973
    }
    responses.add(responses.GET,
                  '%sstreams/summary' % BASE_URL,
                  body=json.dumps(response),
                  status=200,
                  content_type='application/json')

    client = TwitchClient('client id')

    summary = client.streams.get_summary()

    assert len(responses.calls) == 1
    assert isinstance(summary, dict)
    assert summary['channels'] == response['channels']
    assert summary['viewers'] == response['viewers']


@responses.activate
def test_get_featured():
    responses.add(responses.GET,
                  '%sstreams/featured' % BASE_URL,
                  body=json.dumps(example_featured_response),
                  status=200,
                  content_type='application/json')

    client = TwitchClient('client id')

    featured = client.streams.get_featured()

    assert len(responses.calls) == 1
    assert len(featured) == 1
    feature = featured[0]
    assert isinstance(feature, Featured)
    assert feature.title == example_featured_response['featured'][0]['title']
    stream = feature.stream
    assert isinstance(stream, Stream)
    assert stream.id == example_stream_response['stream']['_id']
    assert stream.game == example_stream_response['stream']['game']


@responses.activate
@pytest.mark.parametrize('param,value', [
    ('limit', 101),
])
def test_get_featured_raises_if_wrong_params_are_passed_in(param, value):
    client = TwitchClient('client id')
    kwargs = {param: value}
    with pytest.raises(TwitchException):
        client.streams.get_featured(**kwargs)


@responses.activate
def test_get_followed():
    responses.add(responses.GET,
                  '%sstreams/followed' % BASE_URL,
                  body=json.dumps(example_streams_response),
                  status=200,
                  content_type='application/json')

    client = TwitchClient('client id', 'oauth token')

    streams = client.streams.get_followed()

    assert len(responses.calls) == 1
    assert len(streams) == 1
    stream = streams[0]
    assert isinstance(stream, Stream)
    assert stream.id == example_stream_response['stream']['_id']
    assert stream.game == example_stream_response['stream']['game']

    assert isinstance(stream.channel, Channel)
    assert stream.channel.id == example_stream_response['stream']['channel']['_id']
    assert stream.channel.name == example_stream_response['stream']['channel']['name']


@responses.activate
@pytest.mark.parametrize('param,value', [
    ('limit', 101),
    ('stream_type', 'abcd'),
])
def test_get_followed_raises_if_wrong_params_are_passed_in(param, value):
    client = TwitchClient('client id', 'oauth token')
    kwargs = {param: value}
    with pytest.raises(TwitchException):
        client.streams.get_followed(**kwargs)
