import json
from datetime import datetime

import pytest

import responses

from twitch import TwitchHelix
from twitch.constants import BASE_HELIX_URL, BASE_OAUTH_URL
from twitch.exceptions import TwitchAttributeException, TwitchOAuthException
from twitch.helix.base import APICursor
from twitch.resources import Clip, Follow, Game, Stream, StreamMetadata, Video

example_get_streams_response = {
    "data": [
        {
            "id": "26007494656",
            "user_id": "23161357",
            "game_id": "417752",
            "community_ids": [
                "5181e78f-2280-42a6-873d-758e25a7c313",
                "848d95be-90b3-44a5-b143-6e373754c382",
                "fd0eab99-832a-4d7e-8cc0-04d73deb2e54",
            ],
            "type": "live",
            "title": "Hey Guys - Twitter: @Lirik",
            "viewer_count": 32575,
            "started_at": "2017-08-14T16:08:32Z",
            "language": "en",
            "thumbnail_url": (
                "https://static-cdn.jtvnw.net/previews-ttv/"
                "live_user_lirik-{width}x{height}.jpg"
            ),
        },
    ],
    "pagination": {"cursor": "eyJiIjpudWxsLCJhIjp7Ik9mZnNldCI6MjB9fQ=="},
}

example_get_games_response = {
    "data": [
        {
            "id": "493057",
            "name": "PLAYERUNKNOWN'S BATTLEGROUNDS",
            "box_art_url": (
                "https://static-cdn.jtvnw.net/ttv-boxart/"
                "PLAYERUNKNOWN%27S%20BATTLEGROUNDS-{width}x{height}.jpg"
            ),
        }
    ]
}

example_get_clips_response = {
    "data": [
        {
            "id": "AwkwardHelplessSalamanderSwiftRage",
            "url": "https://clips.twitch.tv/AwkwardHelplessSalamanderSwiftRage",
            "embed_url": "https://clips.twitch.tv/embed?clip=AwkwardHelplessSalamanderSwiftRage",
            "broadcaster_id": "67955580",
            "creator_id": "53834192",
            "video_id": "205586603",
            "game_id": "488191",
            "language": "en",
            "title": "babymetal",
            "view_count": 10,
            "created_at": "2017-11-30T22:34:18Z",
            "thumbnail_url": "https://clips-media-assets.twitch.tv/157589949-preview-480x272.jpg",
        }
    ]
}

example_get_clips_cursor_response = {
    "data": [
        {
            "id": "RandomClip1",
            "url": "https://clips.twitch.tv/AwkwardHelplessSalamanderSwiftRage",
            "embed_url": "https://clips.twitch.tv/embed?clip=RandomClip1",
            "broadcaster_id": "1234",
            "creator_id": "123456",
            "video_id": "1234567",
            "game_id": "33103",
            "language": "en",
            "title": "random1",
            "view_count": 10,
            "created_at": "2017-11-30T22:34:17Z",
            "thumbnail_url": "https://clips-media-assets.twitch.tv/157589949-preview-480x272.jpg",
        },
    ],
    "pagination": {"cursor": "eyJiIjpudWxsLCJhIjoiIn0"},
}

example_get_top_games_response = {
    "data": [
        {
            "id": "493057",
            "name": "PLAYERUNKNOWN'S BATTLEGROUNDS",
            "box_art_url": (
                "https://static-cdn.jtvnw.net/ttv-boxart/"
                "PLAYERUNKNOWN%27S%20BATTLEGROUNDS-{width}x{height}.jpg"
            ),
        },
    ],
    "pagination": {"cursor": "eyJiIjpudWxsLCJhIjp7Ik9mZnNldCI6MjB9fQ=="},
}

example_get_oauth_response = {
    "access_token": "xxxxxx",
    "expires_in": 123456,
    "token_type": "bearer",
}

example_get_oauth_response_with_scopes = {
    "access_token": "xxxxxx",
    "expires_in": 123456,
    "token_type": "bearer",
    "scope":["analytics:read:extensions"]
}

example_get_oauth_error_response = {
    "status": 400,
    "message": "missing client secret",
}

example_get_oauth_bad_request = {
    "status": 401
}

example_get_videos_response = {
    "data": [
        {
            "id": "234482848",
            "user_id": "67955580",
            "title": "-",
            "description": "",
            "created_at": "2018-03-02T20:53:41Z",
            "published_at": "2018-03-02T20:53:41Z",
            "url": "https://www.twitch.tv/videos/234482848",
            "thumbnail_url": "https://example.net/s3_vods/2775/thumb/thumb0-%{width}x%{height}.jpg",
            "viewable": "public",
            "view_count": 142,
            "language": "en",
            "type": "archive",
            "duration": "3h8m33s",
        }
    ],
}

example_get_videos_cursor_response = {
    "data": [
        {
            "id": "234482848",
            "user_id": "67955580",
            "title": "-",
            "description": "",
            "created_at": "2018-03-02T20:53:41Z",
            "published_at": "2018-03-02T20:53:41Z",
            "url": "https://www.twitch.tv/videos/234482848",
            "thumbnail_url": "https://example.net/s3_vods/2775/thumb/thumb0-%{width}x%{height}.jpg",
            "viewable": "public",
            "view_count": 142,
            "language": "en",
            "type": "archive",
            "duration": "3h8m33s",
        }
    ],
    "pagination": {"cursor": "eyJiIjpudWxsLCJhIjoiMTUwMzQ0MTc3NjQyNDQyMjAwMCJ9"},
}


example_get_streams_metadata_response = {
    "data": [
        {
            "user_id": "23161357",
            "game_id": "488552",
            "overwatch": {
                "broadcaster": {
                    "hero": {
                        "role": "Offense",
                        "name": "Soldier 76",
                        "ability": "Heavy Pulse Rifle",
                    }
                }
            },
            "hearthstone": None,
        }
    ],
    "pagination": {"cursor": "eyJiIjpudWxsLCJhIjp7Ik9mZnNldCI6MjB9fQ=="},
}


example_get_user_follows_response = {
    "total": 12345,
    "data": [
        {
            "from_id": "171003792",
            "to_id": "23161357",
            "followed_at": "2017-08-22T22:55:24Z",
        },
    ],
    "pagination": {"cursor": "eyJiIjpudWxsLCJhIjoiMTUwMzQ0MTc3NjQyNDQyMjAwMCJ9"},
}


@responses.activate
def test_get_oauth_returns_oauth_token():
    responses.add(
        responses.POST,
        "{}token".format(BASE_OAUTH_URL),
        body=json.dumps(example_get_oauth_response),
        status=200,
        content_type="application/json",
    )

    client = TwitchHelix("client id", client_secret="client secret")
    client.get_oauth()

    assert client._oauth_token

@responses.activate
def test_get_oauth_returns_oauth_token_with_scopes():
    responses.add(
        responses.POST,
        "{}token".format(BASE_OAUTH_URL),
        body=json.dumps(example_get_oauth_response),
        status=200,
        content_type="application/json",
    )

    client = TwitchHelix("client id", client_secret="client secret",scopes=['analytics:read:extensions'])
    client.get_oauth()

@responses.activate
def test_get_oauth_raises_oauth_exception_bad_request():
    responses.add(
        responses.POST,
        "{}token".format(BASE_OAUTH_URL),
        body=json.dumps(example_get_oauth_error_response),
        status=400,
        content_type="application/json",
    )

    client = TwitchHelix("client id",client_secret='client secret')
    with pytest.raises(TwitchOAuthException):
        client.get_oauth()

@responses.activate
def test_get_oauth_raises_oauth_exception_worse_request():
    responses.add(
        responses.POST,
        "{}token".format(BASE_OAUTH_URL),
        body=json.dumps(example_get_oauth_bad_request),
        status=401,
        content_type="application/json",
    )

    client = TwitchHelix("client id",client_secret='client secret')
    with pytest.raises(TwitchOAuthException):
        client.get_oauth()

def test_get_oauth_raises_oauth_exception_missing_secret():
    client = TwitchHelix("client id")
    with pytest.raises(TwitchOAuthException):
        client.get_oauth()


@responses.activate
def test_get_streams_returns_api_cursor():
    responses.add(
        responses.GET,
        "{}streams".format(BASE_HELIX_URL),
        body=json.dumps(example_get_streams_response),
        status=200,
        content_type="application/json",
    )

    client = TwitchHelix("client id")
    streams = client.get_streams()

    assert len(responses.calls) == 1
    assert isinstance(streams, APICursor)


@responses.activate
def test_get_streams_next_returns_stream_object():
    responses.add(
        responses.GET,
        "{}streams".format(BASE_HELIX_URL),
        body=json.dumps(example_get_streams_response),
        status=200,
        content_type="application/json",
    )

    client = TwitchHelix("client id")
    streams = client.get_streams()

    stream = streams.next()

    assert len(responses.calls) == 1
    assert isinstance(streams, APICursor)
    assert streams._cursor == example_get_streams_response["pagination"]["cursor"]

    assert isinstance(stream, Stream)
    assert stream.id == example_get_streams_response["data"][0]["id"]
    assert stream.game_id == example_get_streams_response["data"][0]["game_id"]
    assert stream.title == example_get_streams_response["data"][0]["title"]
    assert stream.started_at == datetime(2017, 8, 14, 16, 8, 32)


@responses.activate
def test_get_streams_passes_all_params_to_request():
    responses.add(
        responses.GET,
        "{}streams".format(BASE_HELIX_URL),
        body=json.dumps(example_get_streams_response),
        status=200,
        content_type="application/json",
    )

    client = TwitchHelix("client id")
    streams = client.get_streams(
        after="eyJiIjpudWxsLCJhIjp7Ik9mZnNldCI6MjB9fQ==",
        before="eyJiIjp7Ik9mZnNldCI6MH0sImEiOnsiT2Zmc2V0Ijo0MH19==",
        community_ids=[
            "848d95be-90b3-44a5-b143-6e373754c382",
            "fd0eab99-832a-4d7e-8cc0-04d73deb2e54",
        ],
        page_size=100,
        game_ids=["417752", "29307"],
        languages=["en"],
        user_ids=["23161357"],
        user_logins=["lirik"],
    )

    stream = streams.next()

    assert len(responses.calls) == 1
    assert isinstance(streams, APICursor)
    assert isinstance(stream, Stream)

    url = responses.calls[0].request.url
    assert url.startswith("https://api.twitch.tv/helix/streams?")
    assert "after=eyJiIjpudWxsLCJhIjp7Ik9mZnNldCI6MjB9fQ%3D%3D" in url
    assert "before=eyJiIjp7Ik9mZnNldCI6MH0sImEiOnsiT2Zmc2V0Ijo0MH19%3D%3D" in url
    assert "community_id=848d95be-90b3-44a5-b143-6e373754c382" in url
    assert "community_id=fd0eab99-832a-4d7e-8cc0-04d73deb2e54" in url
    assert "first=100" in url
    assert "game_id=417752" in url
    assert "game_id=29307" in url
    assert "language=en" in url
    assert "user_id=23161357" in url
    assert "user_login=lirik" in url


@responses.activate
@pytest.mark.parametrize(
    "param,value",
    [
        ("community_ids", ["abcd"] * 101),
        ("game_ids", ["12345"] * 101),
        ("languages", ["en"] * 101),
        ("user_ids", ["12345"] * 101),
        ("user_logins", ["lirik"] * 101),
        ("page_size", 101),
    ],
)
def test_get_streams_raises_attribute_exception_for_invalid_params(param, value):
    responses.add(
        responses.GET,
        "{}streams".format(BASE_HELIX_URL),
        body=json.dumps(example_get_streams_response),
        status=200,
        content_type="application/json",
    )

    client = TwitchHelix("client id")

    kwargs = {param: value}
    with pytest.raises(TwitchAttributeException):
        client.get_streams(**kwargs)

    assert len(responses.calls) == 0


@responses.activate
def test_get_games_returns_list_of_game_objects():
    responses.add(
        responses.GET,
        "{}games".format(BASE_HELIX_URL),
        body=json.dumps(example_get_games_response),
        status=200,
        content_type="application/json",
    )

    client = TwitchHelix("client id")
    games = client.get_games()

    assert len(responses.calls) == 1
    assert isinstance(games, list)
    game = games[0]
    assert isinstance(game, Game)
    assert game.id == example_get_games_response["data"][0]["id"]
    assert game.name == example_get_games_response["data"][0]["name"]


@responses.activate
def test_get_games_passes_all_params_to_request():
    responses.add(
        responses.GET,
        "{}games".format(BASE_HELIX_URL),
        body=json.dumps(example_get_games_response),
        status=200,
        content_type="application/json",
    )

    client = TwitchHelix("client id")
    games = client.get_games(
        game_ids=["23161357", "12345678"],
        names=["PLAYERUNKNOWN'S BATTLEGROUNDS", "World of Warcraft"],
    )

    assert len(responses.calls) == 1
    assert isinstance(games, list)
    assert isinstance(games[0], Game)
    url = responses.calls[0].request.url
    assert url.startswith("https://api.twitch.tv/helix/games?")
    assert "id=23161357" in url
    assert "id=12345678" in url
    assert "name=PLAYERUNKNOWN%27S+BATTLEGROUNDS" in url
    assert "name=World+of+Warcraft" in url


@responses.activate
@pytest.mark.parametrize(
    "param,value", [("game_ids", ["12345"] * 101), ("names", ["abcd"] * 101)]
)
def test_get_games_raises_attribute_exception_for_invalid_params(param, value):
    responses.add(
        responses.GET,
        "{}games".format(BASE_HELIX_URL),
        body=json.dumps(example_get_games_response),
        status=200,
        content_type="application/json",
    )

    client = TwitchHelix("client id")

    kwargs = {param: value}
    with pytest.raises(TwitchAttributeException):
        client.get_games(**kwargs)

    assert len(responses.calls) == 0


@responses.activate
def test_get_clips_returns_list_of_clip_objects_when_clip_ids_are_set():
    responses.add(
        responses.GET,
        "{}clips".format(BASE_HELIX_URL),
        body=json.dumps(example_get_clips_response),
        status=200,
        content_type="application/json",
    )

    client = TwitchHelix("client id")
    clips = client.get_clips(clip_ids=["AwkwardHelplessSalamanderSwiftRage"])

    assert len(responses.calls) == 1
    assert isinstance(clips, list)
    clip = clips[0]
    assert isinstance(clip, Clip)
    assert clip.id == example_get_clips_response["data"][0]["id"]
    assert (
        clip.broadcaster_id == example_get_clips_response["data"][0]["broadcaster_id"]
    )
    assert clip.created_at == datetime(2017, 11, 30, 22, 34, 18)


@responses.activate
def test_get_clips_passes_correct_params_when_clip_ids_are_set():
    responses.add(
        responses.GET,
        "{}clips".format(BASE_HELIX_URL),
        body=json.dumps(example_get_clips_response),
        status=200,
        content_type="application/json",
    )

    client = TwitchHelix("client id")
    clips = client.get_clips(clip_ids=["AwkwardHelplessSalamanderSwiftRage"])

    assert len(responses.calls) == 1
    assert isinstance(clips, list)
    clip = clips[0]
    assert isinstance(clip, Clip)
    assert responses.calls[0].request.url == (
        "https://api.twitch.tv/helix/clips?id=AwkwardHelplessSalamanderSwiftRage"
    )


@responses.activate
@pytest.mark.parametrize(
    "param,value",
    [
        ("game_id", ["23161357", "12345678"]),
        ("broadcaster_id", ["23161357", "12345678"]),
    ],
)
def test_get_clips_next_returns_clip_object(param, value):
    responses.add(
        responses.GET,
        "{}clips".format(BASE_HELIX_URL),
        body=json.dumps(example_get_clips_cursor_response),
        status=200,
        content_type="application/json",
    )

    client = TwitchHelix("client id")

    kwargs = {param: value}
    clips = client.get_clips(**kwargs)
    clip = clips.next()

    assert len(responses.calls) == 1
    assert isinstance(clips, APICursor)
    assert clips._cursor == example_get_clips_cursor_response["pagination"]["cursor"]

    assert isinstance(clip, Clip)
    assert clip.id == example_get_clips_cursor_response["data"][0]["id"]
    assert (
        clip.broadcaster_id
        == example_get_clips_cursor_response["data"][0]["broadcaster_id"]
    )
    assert clip.created_at == datetime(2017, 11, 30, 22, 34, 17)


@responses.activate
@pytest.mark.parametrize(
    "param,value", [("game_id", "23161357"), ("broadcaster_id", "23161357")]
)
def test_get_clips_passes_correct_params_when_broadcaster_or_game_is_set(param, value):
    responses.add(
        responses.GET,
        "{}clips".format(BASE_HELIX_URL),
        body=json.dumps(example_get_clips_cursor_response),
        status=200,
        content_type="application/json",
    )

    client = TwitchHelix("client id")
    kwargs = {
        param: value,
        "after": "eyJiIjpudWxsLCJhIjp7Ik9mZnNldCI6MjB9fQ==",
        "before": "eyJiIjp7Ik9mZnNldCI6MH0sImEiOnsiT2Zmc2V0Ijo0MH19==",
        "page_size": 100,
    }
    clips = client.get_clips(**kwargs)
    clip = clips.next()

    assert len(responses.calls) == 1
    assert isinstance(clips, APICursor)
    assert isinstance(clip, Clip)

    url = responses.calls[0].request.url
    assert url.startswith("https://api.twitch.tv/helix/clips?")
    assert "{}=23161357".format(param) in url
    assert "after=eyJiIjpudWxsLCJhIjp7Ik9mZnNldCI6MjB9fQ%3D%3D" in url
    assert "before=eyJiIjp7Ik9mZnNldCI6MH0sImEiOnsiT2Zmc2V0Ijo0MH19%3D%3D" in url
    assert "first=100" in url


@responses.activate
def test_get_clips_raises_attribute_exception_for_invalid_clip_ids():
    responses.add(
        responses.GET,
        "{}clips".format(BASE_HELIX_URL),
        body=json.dumps(example_get_clips_response),
        status=200,
        content_type="application/json",
    )

    client = TwitchHelix("client id")
    kwargs = {"clip_ids": ["12345"] * 101}
    with pytest.raises(TwitchAttributeException):
        client.get_clips(**kwargs)

    assert len(responses.calls) == 0


@responses.activate
def test_get_clips_raises_attribute_exception_if_no_param_is_set():
    responses.add(
        responses.GET,
        "{}clips".format(BASE_HELIX_URL),
        body=json.dumps(example_get_clips_response),
        status=200,
        content_type="application/json",
    )

    client = TwitchHelix("client id")
    with pytest.raises(TwitchAttributeException) as e:
        client.get_clips()

    assert (
        "At least one of the following parameters must be provided "
        "[broadcaster_id, clip_ids, game_id]"
    ) in str(e)
    assert len(responses.calls) == 0


@responses.activate
def test_get_top_games_returns_api_cursor():
    responses.add(
        responses.GET,
        "{}games/top".format(BASE_HELIX_URL),
        body=json.dumps(example_get_top_games_response),
        status=200,
        content_type="application/json",
    )

    client = TwitchHelix("client id")
    games = client.get_top_games()

    assert len(responses.calls) == 1
    assert isinstance(games, APICursor)


@responses.activate
def test_get_top_games_next_returns_game_object():
    responses.add(
        responses.GET,
        "{}games/top".format(BASE_HELIX_URL),
        body=json.dumps(example_get_top_games_response),
        status=200,
        content_type="application/json",
    )

    client = TwitchHelix("client id")
    games = client.get_top_games()

    game = games.next()

    assert len(responses.calls) == 1
    assert isinstance(games, APICursor)
    assert games._cursor == example_get_top_games_response["pagination"]["cursor"]

    assert isinstance(game, Game)
    assert game.id == example_get_top_games_response["data"][0]["id"]
    assert game.name == example_get_top_games_response["data"][0]["name"]


@responses.activate
def test_get_top_games_passes_all_params_to_request():
    responses.add(
        responses.GET,
        "{}games/top".format(BASE_HELIX_URL),
        body=json.dumps(example_get_top_games_response),
        status=200,
        content_type="application/json",
    )

    client = TwitchHelix("client id")
    games = client.get_top_games(
        after="eyJiIjpudWxsLCJhIjp7Ik9mZnNldCI6MjB9fQ==",
        before="eyJiIjp7Ik9mZnNldCI6MH0sImEiOnsiT2Zmc2V0Ijo0MH19==",
        page_size=100,
    )

    game = games.next()

    assert len(responses.calls) == 1
    assert isinstance(games, APICursor)
    assert isinstance(game, Game)

    url = responses.calls[0].request.url
    assert url.startswith("https://api.twitch.tv/helix/games/top?")
    assert "after=eyJiIjpudWxsLCJhIjp7Ik9mZnNldCI6MjB9fQ%3D%3D" in url
    assert "before=eyJiIjp7Ik9mZnNldCI6MH0sImEiOnsiT2Zmc2V0Ijo0MH19%3D%3D" in url
    assert "first=100" in url


@responses.activate
def test_get_top_games_raises_attribute_exception_for_invalid_params():
    responses.add(
        responses.GET,
        "{}games/top".format(BASE_HELIX_URL),
        body=json.dumps(example_get_top_games_response),
        status=200,
        content_type="application/json",
    )

    client = TwitchHelix("client id")

    kwargs = {"page_size": 101}
    with pytest.raises(TwitchAttributeException):
        client.get_top_games(**kwargs)

    assert len(responses.calls) == 0


@responses.activate
def test_get_videos_returns_list_of_video_objects_when_video_ids_are_set():
    responses.add(
        responses.GET,
        "{}videos".format(BASE_HELIX_URL),
        body=json.dumps(example_get_videos_response),
        status=200,
        content_type="application/json",
    )

    client = TwitchHelix("client id")
    videos = client.get_videos(video_ids=["234482848"])

    assert len(responses.calls) == 1
    assert isinstance(videos, list)
    video = videos[0]
    assert isinstance(video, Video)
    assert video.id == example_get_videos_response["data"][0]["id"]
    assert video.title == example_get_videos_response["data"][0]["title"]
    assert video.created_at == datetime(2018, 3, 2, 20, 53, 41)


@responses.activate
def test_get_videos_passes_correct_params_when_video_ids_are_set():
    responses.add(
        responses.GET,
        "{}videos".format(BASE_HELIX_URL),
        body=json.dumps(example_get_videos_response),
        status=200,
        content_type="application/json",
    )

    client = TwitchHelix("client id")
    videos = client.get_videos(video_ids=["234482848"])

    assert len(responses.calls) == 1
    assert isinstance(videos, list)
    video = videos[0]
    assert isinstance(video, Video)
    assert (
        responses.calls[0].request.url
        == "https://api.twitch.tv/helix/videos?id=234482848"
    )


@responses.activate
@pytest.mark.parametrize(
    "param,value",
    [("game_id", ["23161357", "12345678"]), ("user_id", ["23161357", "12345678"])],
)
def test_get_videos_next_returns_video_object(param, value):
    responses.add(
        responses.GET,
        "{}videos".format(BASE_HELIX_URL),
        body=json.dumps(example_get_videos_cursor_response),
        status=200,
        content_type="application/json",
    )

    client = TwitchHelix("client id")

    kwargs = {param: value}
    videos = client.get_videos(**kwargs)
    video = videos.next()

    assert len(responses.calls) == 1
    assert isinstance(videos, APICursor)
    assert videos._cursor == example_get_videos_cursor_response["pagination"]["cursor"]

    assert isinstance(video, Video)
    assert video.id == example_get_videos_cursor_response["data"][0]["id"]
    assert video.title == example_get_videos_response["data"][0]["title"]
    assert video.created_at == datetime(2018, 3, 2, 20, 53, 41)


@responses.activate
@pytest.mark.parametrize(
    "param,value", [("game_id", "23161357"), ("user_id", "23161357")]
)
def test_get_videos_passes_correct_params_when_user_or_game_is_set(param, value):
    responses.add(
        responses.GET,
        "{}videos".format(BASE_HELIX_URL),
        body=json.dumps(example_get_videos_cursor_response),
        status=200,
        content_type="application/json",
    )

    client = TwitchHelix("client id")
    kwargs = {
        param: value,
        "after": "eyJiIjpudWxsLCJhIjp7Ik9mZnNldCI6MjB9fQ==",
        "before": "eyJiIjp7Ik9mZnNldCI6MH0sImEiOnsiT2Zmc2V0Ijo0MH19==",
        "page_size": 100,
        "language": "en",
    }
    videos = client.get_videos(**kwargs)
    video = videos.next()

    assert len(responses.calls) == 1
    assert isinstance(videos, APICursor)
    assert isinstance(video, Video)

    url = responses.calls[0].request.url
    url.startswith("https://api.twitch.tv/helix/videos?")
    assert "{}=23161357".format(param) in url
    assert "after=eyJiIjpudWxsLCJhIjp7Ik9mZnNldCI6MjB9fQ%3D%3D" in url
    assert "before=eyJiIjp7Ik9mZnNldCI6MH0sImEiOnsiT2Zmc2V0Ijo0MH19%3D%3D" in url
    assert "first=100" in url
    assert "language=en" in url
    assert "period=all" in url
    assert "sort=time" in url
    assert "type=all" in url


@responses.activate
def test_get_videos_raises_attribute_exception_for_invalid_video_ids():
    responses.add(
        responses.GET,
        "{}videos".format(BASE_HELIX_URL),
        body=json.dumps(example_get_videos_response),
        status=200,
        content_type="application/json",
    )

    client = TwitchHelix("client id")
    kwargs = {"video_ids": ["12345"] * 101}
    with pytest.raises(TwitchAttributeException):
        client.get_videos(**kwargs)

    assert len(responses.calls) == 0


@responses.activate
@pytest.mark.parametrize(
    "param,value",
    [
        ("page_size", 101),
        ("period", "pogchamp"),
        ("sort", "pogchamp"),
        ("video_type", "pogchamp"),
    ],
)
def test_get_videos_raises_attribute_exception_for_invalid_params(param, value):
    responses.add(
        responses.GET,
        "{}videos".format(BASE_HELIX_URL),
        body=json.dumps(example_get_videos_cursor_response),
        status=200,
        content_type="application/json",
    )

    client = TwitchHelix("client id")

    kwargs = {"game_id": "123456", param: value}
    with pytest.raises(TwitchAttributeException):
        client.get_videos(**kwargs)

    assert len(responses.calls) == 0


@responses.activate
def test_get_streams_metadata_returns_api_cursor():
    responses.add(
        responses.GET,
        "{}streams/metadata".format(BASE_HELIX_URL),
        body=json.dumps(example_get_streams_metadata_response),
        status=200,
        content_type="application/json",
    )

    client = TwitchHelix("client id")
    streams_metadata = client.get_streams_metadata()

    assert len(responses.calls) == 1
    assert isinstance(streams_metadata, APICursor)


@responses.activate
def test_get_streams_metadata_next_returns_stream_metadata_object():
    responses.add(
        responses.GET,
        "{}streams/metadata".format(BASE_HELIX_URL),
        body=json.dumps(example_get_streams_metadata_response),
        status=200,
        content_type="application/json",
    )

    client = TwitchHelix("client id")
    streams_metadata = client.get_streams_metadata()

    metadata = streams_metadata.next()

    assert len(responses.calls) == 1
    assert isinstance(streams_metadata, APICursor)
    assert (
        streams_metadata._cursor
        == example_get_streams_metadata_response["pagination"]["cursor"]
    )

    assert isinstance(metadata, StreamMetadata)
    assert (
        metadata.user_id == example_get_streams_metadata_response["data"][0]["user_id"]
    )
    assert (
        metadata.game_id == example_get_streams_metadata_response["data"][0]["game_id"]
    )


@responses.activate
def test_get_streams_metadata_passes_all_params_to_request():
    responses.add(
        responses.GET,
        "{}streams/metadata".format(BASE_HELIX_URL),
        body=json.dumps(example_get_streams_metadata_response),
        status=200,
        content_type="application/json",
    )

    client = TwitchHelix("client id")
    streams_metadata = client.get_streams_metadata(
        after="eyJiIjpudWxsLCJhIjp7Ik9mZnNldCI6MjB9fQ==",
        before="eyJiIjp7Ik9mZnNldCI6MH0sImEiOnsiT2Zmc2V0Ijo0MH19==",
        community_ids=[
            "848d95be-90b3-44a5-b143-6e373754c382",
            "fd0eab99-832a-4d7e-8cc0-04d73deb2e54",
        ],
        page_size=100,
        game_ids=["417752", "29307"],
        languages=["en"],
        user_ids=["23161357"],
        user_logins=["lirik"],
    )

    metadata = streams_metadata.next()

    assert len(responses.calls) == 1
    assert isinstance(streams_metadata, APICursor)
    assert isinstance(metadata, StreamMetadata)

    url = responses.calls[0].request.url
    assert url.startswith("https://api.twitch.tv/helix/streams/metadata?")
    assert "after=eyJiIjpudWxsLCJhIjp7Ik9mZnNldCI6MjB9fQ%3D%3D" in url
    assert "before=eyJiIjp7Ik9mZnNldCI6MH0sImEiOnsiT2Zmc2V0Ijo0MH19%3D%3D" in url
    assert "community_id=848d95be-90b3-44a5-b143-6e373754c382" in url
    assert "community_id=fd0eab99-832a-4d7e-8cc0-04d73deb2e54" in url
    assert "first=100" in url
    assert "game_id=417752" in url
    assert "game_id=29307" in url
    assert "language=en" in url
    assert "user_id=23161357" in url
    assert "user_login=lirik" in url


@responses.activate
@pytest.mark.parametrize(
    "param,value",
    [
        ("community_ids", ["abcd"] * 101),
        ("game_ids", ["12345"] * 101),
        ("languages", ["en"] * 101),
        ("user_ids", ["12345"] * 101),
        ("user_logins", ["lirik"] * 101),
        ("page_size", 101),
    ],
)
def test_get_streams_metadata_raises_attribute_exception_for_invalid_params(
    param, value
):
    responses.add(
        responses.GET,
        "{}streams/metadata".format(BASE_HELIX_URL),
        body=json.dumps(example_get_streams_metadata_response),
        status=200,
        content_type="application/json",
    )

    client = TwitchHelix("client id")

    kwargs = {param: value}
    with pytest.raises(TwitchAttributeException):
        client.get_streams_metadata(**kwargs)

    assert len(responses.calls) == 0


@responses.activate
def test_get_user_follows_returns_api_cursor():
    responses.add(
        responses.GET,
        "{}users/follows".format(BASE_HELIX_URL),
        body=json.dumps(example_get_user_follows_response),
        status=200,
        content_type="application/json",
    )

    client = TwitchHelix("client id")
    user_follows = client.get_user_follows(to_id=23161357)

    assert len(responses.calls) == 1
    assert isinstance(user_follows, APICursor)


@responses.activate
def test_get_user_follows_next_returns_follow_object():
    responses.add(
        responses.GET,
        "{}users/follows".format(BASE_HELIX_URL),
        body=json.dumps(example_get_user_follows_response),
        status=200,
        content_type="application/json",
    )

    client = TwitchHelix("client id")
    user_follows = client.get_user_follows(to_id=23161357)

    follow = user_follows.next()

    assert len(responses.calls) == 1
    assert isinstance(user_follows, APICursor)
    assert (
        user_follows.cursor == example_get_user_follows_response["pagination"]["cursor"]
    )
    assert user_follows.total == example_get_user_follows_response["total"]

    assert isinstance(follow, Follow)
    assert follow.from_id == example_get_user_follows_response["data"][0]["from_id"]
    assert follow.to_id == example_get_user_follows_response["data"][0]["to_id"]
    assert follow.followed_at == datetime(2017, 8, 22, 22, 55, 24)


@responses.activate
def test_get_user_follows_raises_attribute_exception_if_no_param_is_set():
    responses.add(
        responses.GET,
        "{}users/follows".format(BASE_HELIX_URL),
        body=json.dumps(example_get_clips_response),
        status=200,
        content_type="application/json",
    )

    client = TwitchHelix("client id")
    with pytest.raises(TwitchAttributeException):
        client.get_user_follows()
    assert len(responses.calls) == 0


@responses.activate
def test_get_user_follows_passes_all_params_to_request():
    responses.add(
        responses.GET,
        "{}users/follows".format(BASE_HELIX_URL),
        body=json.dumps(example_get_streams_metadata_response),
        status=200,
        content_type="application/json",
    )

    client = TwitchHelix("client id")
    user_follows = client.get_user_follows(
        after="eyJiIjpudWxsLCJhIjp7Ik9mZnNldCI6MjB9fQ==",
        page_size=100,
        from_id=23161357,
        to_id=12345678,
    )

    follow = user_follows.next()

    assert len(responses.calls) == 1
    assert isinstance(user_follows, APICursor)
    assert isinstance(follow, Follow)

    url = responses.calls[0].request.url
    assert url.startswith("https://api.twitch.tv/helix/users/follows?")
    assert "after=eyJiIjpudWxsLCJhIjp7Ik9mZnNldCI6MjB9fQ%3D%3D" in url
    assert "first=100" in url
    assert "from_id=23161357" in url
    assert "to_id=12345678" in url


@responses.activate
def test_get_user_follows_raises_attribute_exception_for_invalid_params():
    responses.add(
        responses.GET,
        "{}users/follows".format(BASE_HELIX_URL),
        body=json.dumps(example_get_top_games_response),
        status=200,
        content_type="application/json",
    )

    client = TwitchHelix("client id")

    kwargs = {"from_id": 23161357, "page_size": 101}
    with pytest.raises(TwitchAttributeException):
        client.get_user_follows(**kwargs)

    assert len(responses.calls) == 0
