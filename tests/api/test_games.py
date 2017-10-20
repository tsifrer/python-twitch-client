import json

import pytest

import responses

from twitch.client import TwitchClient
from twitch.constants import BASE_URL
from twitch.exceptions import TwitchAttributeException
from twitch.resources import Game, TopGame


example_top_games_response = {
    '_total': 1157,
    'top': [{
        'channels': 953,
        'viewers': 171708,
        'game': {
            '_id': 32399,
            'box': {
                'large': ('https://static-cdn.jtvnw.net/ttv-boxart/'
                          'Counter-Strike:%20Global%20Offensive-272x380.jpg'),
                'medium': ('https://static-cdn.jtvnw.net/ttv-boxart/'
                           'Counter-Strike:%20Global%20Offensive-136x190.jpg'),
                'small': ('https://static-cdn.jtvnw.net/ttv-boxart/'
                          'Counter-Strike:%20Global%20Offensive-52x72.jpg'),
                'template': ('https://static-cdn.jtvnw.net/ttv-boxart/Counter-St'
                             'rike:%20Global%20Offensive-{width}x{height}.jpg')
            },
            'giantbomb_id': 36113,
            'logo': {
                'large': ('https://static-cdn.jtvnw.net/ttv-logoart/'
                          'Counter-Strike:%20Global%20Offensive-240x144.jpg'),
                'medium': ('https://static-cdn.jtvnw.net/ttv-logoart/'
                           'Counter-Strike:%20Global%20Offensive-120x72.jpg'),
                'small': ('https://static-cdn.jtvnw.net/ttv-logoart/'
                          'Counter-Strike:%20Global%20Offensive-60x36.jpg'),
                'template': ('https://static-cdn.jtvnw.net/ttv-logoart/Counter-'
                             'Strike:%20Global%20Offensive-{width}x{height}.jpg')
            },
            'name': 'Counter-Strike: Global Offensive',
            'popularity': 170487
        }
    }]
}


@responses.activate
def test_get_top():
    responses.add(responses.GET,
                  '%sgames/top' % BASE_URL,
                  body=json.dumps(example_top_games_response),
                  status=200,
                  content_type='application/json')

    client = TwitchClient('abcd')

    games = client.games.get_top()

    assert len(responses.calls) == 1
    assert len(games) == 1
    assert isinstance(games[0], TopGame)
    game = games[0].game
    assert isinstance(game, Game)
    assert game.id == example_top_games_response['top'][0]['game']['_id']


@responses.activate
@pytest.mark.parametrize('param,value', [
    ('limit', 101),
])
def test_get_top_raises_if_wrong_params_are_passed_in(param, value):
    client = TwitchClient('client id')
    kwargs = {param: value}
    with pytest.raises(TwitchAttributeException):
        client.games.get_top(**kwargs)
