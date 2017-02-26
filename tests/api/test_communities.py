import json

import responses

from twitch.client import TwitchClient
from twitch.constants import BASE_URL
from twitch.resources import Community


example_community = {
   '_id': 'e9f17055-810f-4736-ba40-fba4ac541caa',
   'name': 'DallasTesterCommunity',
}


@responses.activate
def test_get_by_name():
    responses.add(responses.GET,
                  '%scommunities' % BASE_URL,
                  body=json.dumps(example_community),
                  status=200,
                  content_type='application/json')

    client = TwitchClient('client id')

    community = client.communities.get_by_name('spongebob')

    assert len(responses.calls) == 1
    assert isinstance(community, Community)
    assert community.id == example_community['_id']
    assert community.name == example_community['name']


@responses.activate
def test_get_by_id():
    community_id = 'abcd'
    responses.add(responses.GET,
                  '%scommunities/%s' % (BASE_URL, community_id),
                  body=json.dumps(example_community),
                  status=200,
                  content_type='application/json')

    client = TwitchClient('client id')

    community = client.communities.get_by_id(community_id)

    assert len(responses.calls) == 1
    assert isinstance(community, Community)
    assert community.id == example_community['_id']
    assert community.name == example_community['name']


@responses.activate
def test_create():
    responses.add(responses.POST,
                  '%scommunities' % BASE_URL,
                  body=json.dumps(example_community),
                  status=200,
                  content_type='application/json')

    client = TwitchClient('client id')

    community = client.communities.create('spongebob')

    assert len(responses.calls) == 1
    assert isinstance(community, Community)
    assert community.id == example_community['_id']
    assert community.name == example_community['name']


@responses.activate
def test_update():
    community_id = 'abcd'
    responses.add(responses.PUT,
                  '%scommunities/%s' % (BASE_URL, community_id),
                  body=json.dumps(example_community),
                  status=204,
                  content_type='application/json')

    client = TwitchClient('client id')

    client.communities.update(community_id)

    assert len(responses.calls) == 1
