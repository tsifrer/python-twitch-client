import json

import responses

from twitch.client import TwitchClient
from twitch.constants import BASE_URL
from twitch.resources import Channel


example_channel = {
    '_id': 44322889,
    'created_at': '2013-06-03T19:12:02Z',
    'display_name': 'dallas',
}


@responses.activate
def test_get_by_id():
    channel_id = example_channel['_id']
    responses.add(responses.GET,
                  '%schannels/%s' % (BASE_URL, channel_id),
                  body=json.dumps(example_channel),
                  status=200,
                  content_type='application/json')

    client = TwitchClient('abcd')

    channel = client.channels.get_by_id(channel_id)

    assert len(responses.calls) == 1
    assert isinstance(channel, Channel)
    assert channel.id == channel_id
    assert channel.display_name == example_channel['display_name']
