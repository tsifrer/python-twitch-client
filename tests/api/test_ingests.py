import json

import responses

from twitch.client import TwitchClient
from twitch.constants import BASE_URL
from twitch.resources import Ingest


example_response = {"ingests": [{"_id": 24, "name": "EU: Amsterdam, NL"}]}


@responses.activate
def test_get_top():
    responses.add(
        responses.GET,
        "{}ingests".format(BASE_URL),
        body=json.dumps(example_response),
        status=200,
        content_type="application/json",
    )

    client = TwitchClient("abcd")

    ingests = client.ingests.get_server_list()

    assert len(responses.calls) == 1
    assert len(ingests) == 1
    ingest = ingests[0]
    assert isinstance(ingest, Ingest)
    assert ingest.id == example_response["ingests"][0]["_id"]
    assert ingest.name == example_response["ingests"][0]["name"]
