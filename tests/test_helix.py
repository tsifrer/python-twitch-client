import json
from datetime import datetime

import pytest

import responses

from twitch import TwitchHelix
from twitch.constants import BASE_HELIX_URL
from twitch.exceptions import TwitchAttributeException
from twitch.helix import APICursor
from twitch.resources import Game, Stream


example_get_streams_response = {
    'data': [
        {
            'id': '26007494656',
            'user_id': '23161357',
            'game_id': '417752',
            'community_ids': [
                '5181e78f-2280-42a6-873d-758e25a7c313',
                '848d95be-90b3-44a5-b143-6e373754c382',
                'fd0eab99-832a-4d7e-8cc0-04d73deb2e54'
            ],
            'type': 'live',
            'title': 'Hey Guys - Twitter: @Lirik',
            'viewer_count': 32575,
            'started_at': '2017-08-14T16:08:32Z',
            'language': 'en',
            'thumbnail_url': (
                'https://static-cdn.jtvnw.net/previews-ttv/'
                'live_user_lirik-{width}x{height}.jpg'
            )
        },
    ],
    'pagination': {
        'cursor': 'eyJiIjpudWxsLCJhIjp7Ik9mZnNldCI6MjB9fQ=='
    }
}

example_get_games_response = {
    'data': [
        {
            'id': '493057',
            'name': "PLAYERUNKNOWN'S BATTLEGROUNDS",
            'box_art_url': (
                'https://static-cdn.jtvnw.net/ttv-boxart/'
                'PLAYERUNKNOWN%27S%20BATTLEGROUNDS-{width}x{height}.jpg'
            )
        }
    ]
}


@responses.activate
def test_get_streams_returns_api_cursor():
    responses.add(responses.GET,
                  '{}streams'.format(BASE_HELIX_URL),
                  body=json.dumps(example_get_streams_response),
                  status=200,
                  content_type='application/json')

    client = TwitchHelix('client id')
    streams = client.get_streams()

    assert len(responses.calls) == 0
    assert isinstance(streams, APICursor)


@responses.activate
def test_get_streams_next_returns_stream_object():
    responses.add(responses.GET,
                  '{}streams'.format(BASE_HELIX_URL),
                  body=json.dumps(example_get_streams_response),
                  status=200,
                  content_type='application/json')

    client = TwitchHelix('client id')
    streams = client.get_streams()

    stream = streams.next()

    assert len(responses.calls) == 1
    assert isinstance(streams, APICursor)
    assert streams._cursor == example_get_streams_response['pagination']['cursor']

    assert isinstance(stream, Stream)
    assert stream.id == example_get_streams_response['data'][0]['id']
    assert stream.game_id == example_get_streams_response['data'][0]['game_id']
    assert stream.title == example_get_streams_response['data'][0]['title']
    assert stream.started_at == datetime(2017, 8, 14, 16, 8, 32)


@responses.activate
def test_get_streams_passes_all_params_to_request():
    responses.add(responses.GET,
                  '{}streams'.format(BASE_HELIX_URL),
                  body=json.dumps(example_get_streams_response),
                  status=200,
                  content_type='application/json')

    client = TwitchHelix('client id')
    streams = client.get_streams(
        after='eyJiIjpudWxsLCJhIjp7Ik9mZnNldCI6MjB9fQ==',
        before='eyJiIjp7Ik9mZnNldCI6MH0sImEiOnsiT2Zmc2V0Ijo0MH19==',
        community_ids=[
            '848d95be-90b3-44a5-b143-6e373754c382',
            'fd0eab99-832a-4d7e-8cc0-04d73deb2e54'
        ],
        page_size=100,
        game_ids=['417752', '29307'],
        languages=['en'],
        user_ids=['23161357'],
        user_logins=['lirik']
    )

    stream = streams.next()

    assert len(responses.calls) == 1
    assert isinstance(streams, APICursor)
    assert isinstance(stream, Stream)
    assert responses.calls[0].request.url == (
        'https://api.twitch.tv/helix/streams'
        '?after=eyJiIjpudWxsLCJhIjp7Ik9mZnNldCI6MjB9fQ%3D%3D'
        '&before=eyJiIjp7Ik9mZnNldCI6MH0sImEiOnsiT2Zmc2V0Ijo0MH19%3D%3D'
        '&community_id=848d95be-90b3-44a5-b143-6e373754c382'
        '&community_id=fd0eab99-832a-4d7e-8cc0-04d73deb2e54'
        '&first=100'
        '&game_id=417752'
        '&game_id=29307'
        '&language=en'
        '&user_id=23161357'
        '&user_login=lirik'
    )


@responses.activate
@pytest.mark.parametrize('param,value', [
    ('community_ids', ['abcd'] * 101),
    ('game_ids', ['12345'] * 101),
    ('languages', ['en'] * 101),
    ('user_ids', ['12345'] * 101),
    ('user_logins', ['lirik'] * 101),
    ('page_size', 101),
])
def test_get_streams_raises_attribute_exception_for_invalid_params(param, value):
    responses.add(responses.GET,
                  '{}streams'.format(BASE_HELIX_URL),
                  body=json.dumps(example_get_streams_response),
                  status=200,
                  content_type='application/json')

    client = TwitchHelix('client id')

    kwargs = {param: value}
    with pytest.raises(TwitchAttributeException):
        client.get_streams(**kwargs)

    assert len(responses.calls) == 0


@responses.activate
def test_get_games_returns_list_of_game_objects():
    responses.add(responses.GET,
                  '{}games'.format(BASE_HELIX_URL),
                  body=json.dumps(example_get_games_response),
                  status=200,
                  content_type='application/json')

    client = TwitchHelix('client id')
    games = client.get_games()

    assert len(responses.calls) == 1
    assert isinstance(games, list)
    game = games[0]
    assert isinstance(game, Game)
    assert game.id == example_get_games_response['data'][0]['id']
    assert game.name == example_get_games_response['data'][0]['name']


@responses.activate
def test_get_games_passes_all_params_to_request():
    responses.add(responses.GET,
                  '{}games'.format(BASE_HELIX_URL),
                  body=json.dumps(example_get_games_response),
                  status=200,
                  content_type='application/json')

    client = TwitchHelix('client id')
    games = client.get_games(
        game_ids=['23161357', '12345678'],
        names=["PLAYERUNKNOWN'S BATTLEGROUNDS", 'World of Warcraft'],
    )

    assert len(responses.calls) == 1
    assert isinstance(games, list)
    assert isinstance(games[0], Game)
    assert responses.calls[0].request.url == (
        'https://api.twitch.tv/helix/games'
        '?id=23161357'
        '&id=12345678'
        '&name=PLAYERUNKNOWN%27S+BATTLEGROUNDS'
        '&name=World+of+Warcraft'
    )


@responses.activate
@pytest.mark.parametrize('param,value', [
    ('game_ids', ['12345'] * 101),
    ('names', ['abcd'] * 101),
])
def test_get_games_raises_attribute_exception_for_invalid_params(param, value):
    responses.add(responses.GET,
                  '{}games'.format(BASE_HELIX_URL),
                  body=json.dumps(example_get_games_response),
                  status=200,
                  content_type='application/json')

    client = TwitchHelix('client id')

    kwargs = {param: value}
    with pytest.raises(TwitchAttributeException):
        client.get_games(**kwargs)

    assert len(responses.calls) == 0
