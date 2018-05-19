import json

import responses

from twitch.client import TwitchClient
from twitch.constants import BASE_URL
from twitch.resources import Clip

example_clip = {
    "broadcast_id": "25782478272",
    "title": "cold ace",
    "tracking_id": "102382269",
    "url": "https://clips.twitch.tv/OpenUglySnoodVoteNay?tt_medium=clips_api&tt_content=url"
}

example_clips = {'clips': [example_clip]}


@responses.activate
def test_get_by_slug():
    slug = 'OpenUglySnoodVoteNay'

    responses.add(
        responses.GET,
        '{}clips/{}'.format(BASE_URL, slug),
        body=json.dumps(example_clip),
        status=200,
        content_type='application/json'
    )

    client = TwitchClient('client id')
    clip = client.clips.get_by_slug(slug)

    assert isinstance(clip, Clip)
    assert clip.broadcast_id == example_clip['broadcast_id']


@responses.activate
def test_get_top():
    params = {'limit': 1, 'period': 'month'}

    responses.add(
        responses.GET,
        '{}clips/top'.format(BASE_URL),
        body=json.dumps(example_clips),
        status=200,
        content_type='application/json'
    )

    client = TwitchClient('client id')
    clips = client.clips.get_top(**params)

    assert len(clips) == len(example_clips)
    assert isinstance(clips[0], Clip)
    assert clips[0].broadcast_id == example_clips['clips'][0]['broadcast_id']
