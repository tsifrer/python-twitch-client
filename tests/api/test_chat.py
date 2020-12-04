import json

import responses

from twitch.client import TwitchClient
from twitch.constants import BASE_URL

example_emote = {"code": "TwitchLit", "id": 115390}


@responses.activate
def test_get_badges_by_channel():
    channel_id = 7236692
    response = {
        "admin": {
            "alpha": "https://static-cdn.jtvnw.net/chat-badges/admin-alpha.png",
            "image": "https://static-cdn.jtvnw.net/chat-badges/admin.png",
            "svg": "https://static-cdn.jtvnw.net/chat-badges/admin.svg",
        }
    }
    responses.add(
        responses.GET,
        "{}chat/{}/badges".format(BASE_URL, channel_id),
        body=json.dumps(response),
        status=200,
        content_type="application/json",
    )

    client = TwitchClient("client id")

    badges = client.chat.get_badges_by_channel(channel_id)

    assert len(responses.calls) == 1
    assert isinstance(badges, dict)
    assert badges["admin"] == response["admin"]


@responses.activate
def test_get_emoticons_by_set():
    response = {"emoticon_sets": {"19151": [example_emote]}}
    responses.add(
        responses.GET,
        "{}chat/emoticon_images".format(BASE_URL),
        body=json.dumps(response),
        status=200,
        content_type="application/json",
    )

    client = TwitchClient("client id")

    emoticon_sets = client.chat.get_emoticons_by_set()

    assert len(responses.calls) == 1
    assert isinstance(emoticon_sets, dict)
    assert emoticon_sets["emoticon_sets"] == response["emoticon_sets"]
    assert emoticon_sets["emoticon_sets"]["19151"][0] == example_emote


@responses.activate
def test_get_all_emoticons():
    response = {"emoticons": [example_emote]}
    responses.add(
        responses.GET,
        "{}chat/emoticons".format(BASE_URL),
        body=json.dumps(response),
        status=200,
        content_type="application/json",
    )

    client = TwitchClient("client id")

    emoticon_sets = client.chat.get_all_emoticons()

    assert len(responses.calls) == 1
    assert isinstance(emoticon_sets, dict)
    assert emoticon_sets["emoticons"] == response["emoticons"]
    assert emoticon_sets["emoticons"][0] == example_emote
