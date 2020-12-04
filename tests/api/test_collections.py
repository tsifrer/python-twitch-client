import json

import pytest
import responses

from twitch.client import TwitchClient
from twitch.constants import BASE_URL
from twitch.exceptions import TwitchAttributeException
from twitch.resources import Collection, Item

example_collection = {
    "_id": "myIbIFkZphQSbQ",
    "items_count": 3,
    "updated_at": "2017-03-06T18:40:51.855Z",
}

example_item = {
    "_id": "eyJ0eXBlIjoidmlkZW8iLCJpZCI6IjEyMjEzODk0OSJ9",
    "item_id": "122138949",
    "item_type": "video",
    "published_at": "2017-02-14T22:27:54Z",
    "title": "Fanboys Episode 1 w/ Gassy Mexican",
}


@responses.activate
def test_get_metadata():
    collection_id = "abcd"
    responses.add(
        responses.GET,
        "{}collections/{}".format(BASE_URL, collection_id),
        body=json.dumps(example_collection),
        status=200,
        content_type="application/json",
    )

    client = TwitchClient("client id", "oauth token")

    collection = client.collections.get_metadata(collection_id)

    assert len(responses.calls) == 1
    assert isinstance(collection, Collection)
    assert collection.id == example_collection["_id"]
    assert collection.items_count == example_collection["items_count"]


@responses.activate
def test_get():
    collection_id = "abcd"
    response = {"_id": "myIbIFkZphQSbQ", "items": [example_item]}
    responses.add(
        responses.GET,
        "{}collections/{}/items".format(BASE_URL, collection_id),
        body=json.dumps(response),
        status=200,
        content_type="application/json",
    )

    client = TwitchClient("client id", "oauth token")

    items = client.collections.get(collection_id)

    assert len(responses.calls) == 1
    assert len(items) == 1
    item = items[0]
    assert isinstance(item, Item)
    assert item.id == example_item["_id"]
    assert item.title == example_item["title"]


@responses.activate
def test_get_by_channel():
    channel_id = "abcd"
    response = {"_cursor": None, "collections": [example_collection]}
    responses.add(
        responses.GET,
        "{}channels/{}/collections".format(BASE_URL, channel_id),
        body=json.dumps(response),
        status=200,
        content_type="application/json",
    )

    client = TwitchClient("client id", "oauth token")

    collections = client.collections.get_by_channel(channel_id)

    assert len(responses.calls) == 1
    assert len(collections) == 1
    collection = collections[0]
    assert isinstance(collection, Collection)
    assert collection.id == example_collection["_id"]
    assert collection.items_count == example_collection["items_count"]


@responses.activate
@pytest.mark.parametrize("param,value", [("limit", 101)])
def test_get_by_channel_raises_if_wrong_params_are_passed_in(param, value):
    client = TwitchClient("client id", "oauth token")
    kwargs = {param: value}
    with pytest.raises(TwitchAttributeException):
        client.collections.get_by_channel("1234", **kwargs)


@responses.activate
def test_create():
    channel_id = "abcd"
    responses.add(
        responses.POST,
        "{}channels/{}/collections".format(BASE_URL, channel_id),
        body=json.dumps(example_collection),
        status=200,
        content_type="application/json",
    )

    client = TwitchClient("client id", "oauth client")

    collection = client.collections.create(channel_id, "this is title")

    assert len(responses.calls) == 1
    assert isinstance(collection, Collection)
    assert collection.id == example_collection["_id"]
    assert collection.items_count == example_collection["items_count"]


@responses.activate
def test_update():
    collection_id = "abcd"
    responses.add(
        responses.PUT,
        "{}collections/{}".format(BASE_URL, collection_id),
        status=204,
        content_type="application/json",
    )

    client = TwitchClient("client id", "oauth client")

    client.collections.update(collection_id, "this is title")

    assert len(responses.calls) == 1


@responses.activate
def test_create_thumbnail():
    collection_id = "abcd"
    responses.add(
        responses.PUT,
        "{}collections/{}/thumbnail".format(BASE_URL, collection_id),
        status=204,
        content_type="application/json",
    )

    client = TwitchClient("client id", "oauth client")

    client.collections.create_thumbnail(collection_id, "1234")

    assert len(responses.calls) == 1


@responses.activate
def test_delete():
    collection_id = "abcd"
    responses.add(
        responses.DELETE,
        "{}collections/{}".format(BASE_URL, collection_id),
        status=204,
        content_type="application/json",
    )

    client = TwitchClient("client id", "oauth client")

    client.collections.delete(collection_id)

    assert len(responses.calls) == 1


@responses.activate
def test_add_item():
    collection_id = "abcd"
    responses.add(
        responses.PUT,
        "{}collections/{}/items".format(BASE_URL, collection_id),
        body=json.dumps(example_item),
        status=200,
        content_type="application/json",
    )

    client = TwitchClient("client id", "oauth client")

    item = client.collections.add_item(collection_id, "1234", "video")

    assert len(responses.calls) == 1
    assert isinstance(item, Item)
    assert item.id == example_item["_id"]
    assert item.title == example_item["title"]


@responses.activate
def test_delete_item():
    collection_id = "abcd"
    collection_item_id = "1234"
    responses.add(
        responses.DELETE,
        "{}collections/{}/items/{}".format(BASE_URL, collection_id, collection_item_id),
        status=204,
        content_type="application/json",
    )

    client = TwitchClient("client id", "oauth client")

    client.collections.delete_item(collection_id, collection_item_id)

    assert len(responses.calls) == 1


@responses.activate
def test_move_item():
    collection_id = "abcd"
    collection_item_id = "1234"
    responses.add(
        responses.PUT,
        "{}collections/{}/items/{}".format(BASE_URL, collection_id, collection_item_id),
        status=204,
        content_type="application/json",
    )

    client = TwitchClient("client id", "oauth client")

    client.collections.move_item(collection_id, collection_item_id, 3)

    assert len(responses.calls) == 1
