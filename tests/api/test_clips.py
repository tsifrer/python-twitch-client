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

@responses.activate
def test_get_slug():
    slug = 'OpenUglySnoodVoteNay'

    responses.add(
        responses.GET,
        '%sclips/%s' % (BASE_URL, slug),
        body=json.dumps(example_clip),
        status=200,
        content_type='application/json'
    )

    client = TwitchClient('client id')
    clip = client.clips.get_by_slug(slug)

    assert isinstance(clip, Clip)
    assert clip.broadcast_id == example_clip['broadcast_id']
