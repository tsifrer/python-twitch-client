import json
from datetime import datetime

import pytest

import responses

from twitch import TwitchHelix
from twitch.constants import BASE_HELIX_URL
from twitch.exceptions import TwitchAttributeException
from twitch.helix import APICursor
from twitch.resources import Clip, Game, Stream


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


example_get_clips_response = {
    'data': [
        {
            'id': 'AwkwardHelplessSalamanderSwiftRage',
            'url': 'https://clips.twitch.tv/AwkwardHelplessSalamanderSwiftRage',
            'embed_url': 'https://clips.twitch.tv/embed?clip=AwkwardHelplessSalamanderSwiftRage',
            'broadcaster_id': '67955580',
            'creator_id': '53834192',
            'video_id': '205586603',
            'game_id': '488191',
            'language': 'en',
            'title': 'babymetal',
            'view_count': 10,
            'created_at': '2017-11-30T22:34:18Z',
            'thumbnail_url': 'https://clips-media-assets.twitch.tv/157589949-preview-480x272.jpg'
        }
    ]
}

example_get_clips_cursor_response = {
    'data': [
        {
            'id': 'RandomClip1',
            'url': 'https://clips.twitch.tv/AwkwardHelplessSalamanderSwiftRage',
            'embed_url': 'https://clips.twitch.tv/embed?clip=RandomClip1',
            'broadcaster_id': '1234',
            'creator_id': '123456',
            'video_id': '1234567',
            'game_id': '33103',
            'language': 'en',
            'title': 'random1',
            'view_count': 10,
            'created_at': '2017-11-30T22:34:17Z',
            'thumbnail_url': 'https://clips-media-assets.twitch.tv/157589949-preview-480x272.jpg'
        },
    ],
    'pagination': {
        'cursor': 'eyJiIjpudWxsLCJhIjoiIn0'
    }
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


@responses.activate
def test_get_clips_returns_list_of_clip_objects_when_clip_ids_are_set():
    responses.add(responses.GET,
                  '{}clips'.format(BASE_HELIX_URL),
                  body=json.dumps(example_get_clips_response),
                  status=200,
                  content_type='application/json')

    client = TwitchHelix('client id')
    clips = client.get_clips(clip_ids=['AwkwardHelplessSalamanderSwiftRage'])

    assert len(responses.calls) == 1
    assert isinstance(clips, list)
    clip = clips[0]
    assert isinstance(clip, Clip)
    assert clip.id == example_get_clips_response['data'][0]['id']
    assert clip.broadcaster_id == example_get_clips_response['data'][0]['broadcaster_id']
    assert clip.created_at == datetime(2017, 11, 30, 22, 34, 18)


@responses.activate
def test_get_clips_passes_correct_params_when_clip_ids_are_set():
    responses.add(responses.GET,
                  '{}clips'.format(BASE_HELIX_URL),
                  body=json.dumps(example_get_clips_response),
                  status=200,
                  content_type='application/json')

    client = TwitchHelix('client id')
    clips = client.get_clips(clip_ids=['AwkwardHelplessSalamanderSwiftRage'])

    assert len(responses.calls) == 1
    assert isinstance(clips, list)
    clip = clips[0]
    assert isinstance(clip, Clip)
    assert responses.calls[0].request.url == (
        'https://api.twitch.tv/helix/clips'
        '?id=AwkwardHelplessSalamanderSwiftRage'
    )


@responses.activate
@pytest.mark.parametrize('param,value', [
    ('game_id', ['23161357', '12345678']),
    ('broadcaster_id', ['23161357', '12345678']),
])
def test_get_clips_next_returns_clip_object(param, value):
    responses.add(responses.GET,
                  '{}clips'.format(BASE_HELIX_URL),
                  body=json.dumps(example_get_clips_cursor_response),
                  status=200,
                  content_type='application/json')

    client = TwitchHelix('client id')

    kwargs = {param: value}
    clips = client.get_clips(**kwargs)
    clip = clips.next()

    assert len(responses.calls) == 1
    assert isinstance(clips, APICursor)
    assert clips._cursor == example_get_clips_cursor_response['pagination']['cursor']

    assert isinstance(clip, Clip)
    assert clip.id == example_get_clips_cursor_response['data'][0]['id']
    assert clip.broadcaster_id == example_get_clips_cursor_response['data'][0]['broadcaster_id']
    assert clip.created_at == datetime(2017, 11, 30, 22, 34, 17)


@responses.activate
@pytest.mark.parametrize('param,value', [
    ('game_id', '23161357'),
    ('broadcaster_id', '23161357'),
])
def test_get_clips_passes_correct_params_when_broadcaster_or_game_is_set(param, value):
    responses.add(responses.GET,
                  '{}clips'.format(BASE_HELIX_URL),
                  body=json.dumps(example_get_clips_cursor_response),
                  status=200,
                  content_type='application/json')

    client = TwitchHelix('client id')
    kwargs = {
        param: value,
        'after': 'eyJiIjpudWxsLCJhIjp7Ik9mZnNldCI6MjB9fQ==',
        'before': 'eyJiIjp7Ik9mZnNldCI6MH0sImEiOnsiT2Zmc2V0Ijo0MH19==',
        'page_size': 100,
    }
    clips = client.get_clips(**kwargs)
    clip = clips.next()

    assert len(responses.calls) == 1
    assert isinstance(clips, APICursor)
    assert isinstance(clip, Clip)

    assert responses.calls[0].request.url == (
        'https://api.twitch.tv/helix/clips'
        '?{}=23161357'
        '&after=eyJiIjpudWxsLCJhIjp7Ik9mZnNldCI6MjB9fQ%3D%3D'
        '&before=eyJiIjp7Ik9mZnNldCI6MH0sImEiOnsiT2Zmc2V0Ijo0MH19%3D%3D'
        '&first=100'
    ).format(param)


@responses.activate
def test_get_clips_raises_attribute_exception_for_invalid_clip_ids():
    responses.add(responses.GET,
                  '{}clips'.format(BASE_HELIX_URL),
                  body=json.dumps(example_get_clips_response),
                  status=200,
                  content_type='application/json')

    client = TwitchHelix('client id')
    kwargs = {'clip_ids': ['12345'] * 101}
    with pytest.raises(TwitchAttributeException):
        client.get_clips(**kwargs)

    assert len(responses.calls) == 0


@responses.activate
def test_get_clips_raises_attribute_exception_if_no_param_is_set():
    responses.add(responses.GET,
                  '{}clips'.format(BASE_HELIX_URL),
                  body=json.dumps(example_get_clips_response),
                  status=200,
                  content_type='application/json')

    client = TwitchHelix('client id')
    with pytest.raises(TwitchAttributeException) as e:
        client.get_clips()

    assert ('At least one of the following parameters must be provided '
            '[broadcaster_id, clip_ids, game_id]'
            ) in str(e)
    assert len(responses.calls) == 0
