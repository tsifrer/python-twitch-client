import json

import pytest

import responses

from twitch.client import TwitchClient
from twitch.constants import BASE_URL
from twitch.exceptions import TwitchException
from twitch.resources import Channel, Game, Stream


example_channel = {
    '_id': 44322889,
    'name': 'dallas',
}

example_game = {
    '_id': 490422,
    'name': 'StarCraft II',
}

example_stream = {
    '_id': 23932774784,
    'game': 'BATMAN - The Telltale Series',
    'channel': example_channel
}


@responses.activate
def test_channels():
    response = {
        '_total': 2147,
        'channels': [example_channel]
    }
    responses.add(responses.GET,
                  '%ssearch/channels' % BASE_URL,
                  body=json.dumps(response),
                  status=200,
                  content_type='application/json')

    client = TwitchClient('client id')

    channels = client.search.channels('mah query')

    assert len(responses.calls) == 1
    assert len(channels) == 1
    channel = channels[0]
    assert isinstance(channel, Channel)
    assert channel.id == example_channel['_id']
    assert channel.name == example_channel['name']


@responses.activate
@pytest.mark.parametrize('param,value', [
    ('limit', 101),
])
def test_channels_raises_if_wrong_params_are_passed_in(param, value):
    client = TwitchClient('client id')
    kwargs = {param: value}
    with pytest.raises(TwitchException):
        client.search.channels('mah query', **kwargs)


@responses.activate
def test_games():
    response = {
        '_total': 2147,
        'games': [example_game]
    }
    responses.add(responses.GET,
                  '%ssearch/games' % BASE_URL,
                  body=json.dumps(response),
                  status=200,
                  content_type='application/json')

    client = TwitchClient('client id')

    games = client.search.games('mah query')

    assert len(responses.calls) == 1
    assert len(games) == 1
    game = games[0]
    assert isinstance(game, Game)
    assert game.id == example_game['_id']
    assert game.name == example_game['name']


@responses.activate
def test_streams():
    response = {
        '_total': 2147,
        'streams': [example_stream]
    }
    responses.add(responses.GET,
                  '%ssearch/streams' % BASE_URL,
                  body=json.dumps(response),
                  status=200,
                  content_type='application/json')

    client = TwitchClient('client id')

    streams = client.search.streams('mah query')

    assert len(responses.calls) == 1
    assert len(streams) == 1
    stream = streams[0]
    assert isinstance(stream, Stream)
    assert stream.id == example_stream['_id']
    assert stream.game == example_stream['game']

    assert isinstance(stream.channel, Channel)
    assert stream.channel.id == example_channel['_id']
    assert stream.channel.name == example_channel['name']


@responses.activate
@pytest.mark.parametrize('param,value', [
    ('limit', 101),
])
def test_streams_raises_if_wrong_params_are_passed_in(param, value):
    client = TwitchClient('client id')
    kwargs = {param: value}
    with pytest.raises(TwitchException):
        client.search.streams('mah query', **kwargs)
