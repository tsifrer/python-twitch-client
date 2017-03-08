import json

import pytest

import responses

from twitch.client import TwitchClient
from twitch.constants import BASE_URL
from twitch.exceptions import TwitchAttributeException
from twitch.resources import Channel, Community, Follow, Subscription, Team, User, Video


example_user = {
    '_id': '44322889',
    'name': 'dallas',
}

example_channel = {
    '_id': 44322889,
    'name': 'dallas',
}

example_follower = {
    'created_at': '2016-09-16T20:37:39Z',
    'notifications': False,
    'user': example_user
}

example_team = {
    "_id": 10,
    "name": "staff",
}

example_subscription = {
    "_id": "67123294ed8305ce3a8ef09649d2237c5a300590",
    "created_at": "2014-05-19T23:38:53Z",
    "user": example_user
}

example_video = {
   '_id': 'v106400740',
   'description': 'Protect your chat with AutoMod!',
   'fps': {
      '1080p': 23.9767661758746,
   },
}

example_community = {
   '_id': 'e9f17055-810f-4736-ba40-fba4ac541caa',
   'name': 'DallasTesterCommunity',
}


@responses.activate
def test_get():
    responses.add(responses.GET,
                  '%schannels' % BASE_URL,
                  body=json.dumps(example_channel),
                  status=200,
                  content_type='application/json')

    client = TwitchClient('client id', 'oauth token')

    channel = client.channels.get()

    assert len(responses.calls) == 1
    assert isinstance(channel, Channel)
    assert channel.id == example_channel['_id']
    assert channel.name == example_channel['name']


@responses.activate
def test_get_by_id():
    channel_id = example_channel['_id']
    responses.add(responses.GET,
                  '%schannels/%s' % (BASE_URL, channel_id),
                  body=json.dumps(example_channel),
                  status=200,
                  content_type='application/json')

    client = TwitchClient('client id', 'oauth token')

    channel = client.channels.get_by_id(channel_id)

    assert len(responses.calls) == 1
    assert isinstance(channel, Channel)
    assert channel.id == channel_id
    assert channel.name == example_channel['name']


@responses.activate
def test_update():
    channel_id = example_channel['_id']
    responses.add(responses.PUT,
                  '%schannels/%s' % (BASE_URL, channel_id),
                  body=json.dumps(example_channel),
                  status=200,
                  content_type='application/json')

    client = TwitchClient('client id', 'oauth token')

    channel = client.channels.update(channel_id)

    assert len(responses.calls) == 1
    assert isinstance(channel, Channel)
    assert channel.id == channel_id
    assert channel.name == example_channel['name']


@responses.activate
def test_get_editors():
    channel_id = example_channel['_id']
    response = {
        "users": [example_user]
    }
    responses.add(responses.GET,
                  '%schannels/%s/editors' % (BASE_URL, channel_id),
                  body=json.dumps(response),
                  status=200,
                  content_type='application/json')

    client = TwitchClient('client id', 'oauth token')

    users = client.channels.get_editors(channel_id)

    assert len(responses.calls) == 1
    assert len(users) == 1
    user = users[0]
    assert isinstance(user, User)
    assert user.id == example_user['_id']
    assert user.name == example_user['name']


@responses.activate
def test_get_followers():
    channel_id = example_channel['_id']
    response = {
        "_cursor": "1481675542963907000",
        "_total": 41,
        "follows": [example_follower]
    }
    responses.add(responses.GET,
                  '%schannels/%s/follows' % (BASE_URL, channel_id),
                  body=json.dumps(response),
                  status=200,
                  content_type='application/json')

    client = TwitchClient('client id')

    followers = client.channels.get_followers(channel_id)

    assert len(responses.calls) == 1
    assert len(followers) == 1
    follow = followers[0]
    assert isinstance(follow, Follow)
    assert follow.notifications == example_follower['notifications']
    assert isinstance(follow.user, User)
    assert follow.user.id == example_user['_id']
    assert follow.user.name == example_user['name']


@responses.activate
@pytest.mark.parametrize('param,value', [
    ('limit', 101),
    ('direction', 'abcd')
])
def test_get_followers_raises_if_wrong_params_are_passed_in(param, value):
    client = TwitchClient('client id')
    kwargs = {param: value}
    with pytest.raises(TwitchAttributeException):
        client.channels.get_followers('1234', **kwargs)


@responses.activate
def test_get_teams():
    channel_id = example_channel['_id']
    response = {
        "teams": [example_team]
    }
    responses.add(responses.GET,
                  '%schannels/%s/teams' % (BASE_URL, channel_id),
                  body=json.dumps(response),
                  status=200,
                  content_type='application/json')

    client = TwitchClient('client id')

    teams = client.channels.get_teams(channel_id)

    assert len(responses.calls) == 1
    assert len(teams) == 1
    team = teams[0]
    assert isinstance(team, Team)
    assert team.id == example_team['_id']
    assert team.name == example_team['name']


@responses.activate
def test_get_subscribers():
    channel_id = example_channel['_id']
    response = {
        "_total": 1,
        "subscriptions": [example_subscription]
    }
    responses.add(responses.GET,
                  '%schannels/%s/subscriptions' % (BASE_URL, channel_id),
                  body=json.dumps(response),
                  status=200,
                  content_type='application/json')

    client = TwitchClient('client id', 'oauth token')

    subscribers = client.channels.get_subscribers(channel_id)

    assert len(responses.calls) == 1
    assert len(subscribers) == 1
    subscribe = subscribers[0]
    assert isinstance(subscribe, Subscription)
    assert subscribe.id == example_subscription['_id']
    assert isinstance(subscribe.user, User)
    assert subscribe.user.id == example_user['_id']
    assert subscribe.user.name == example_user['name']


@responses.activate
@pytest.mark.parametrize('param,value', [
    ('limit', 101),
    ('direction', 'abcd')
])
def test_get_subscribers_raises_if_wrong_params_are_passed_in(param, value):
    client = TwitchClient('client id', 'oauth token')
    kwargs = {param: value}
    with pytest.raises(TwitchAttributeException):
        client.channels.get_subscribers('1234', **kwargs)


@responses.activate
def test_check_subscription_by_user():
    channel_id = example_channel['_id']
    user_id = example_user['_id']
    responses.add(responses.GET,
                  '%schannels/%s/subscriptions/%s' % (BASE_URL, channel_id, user_id),
                  body=json.dumps(example_subscription),
                  status=200,
                  content_type='application/json')

    client = TwitchClient('client id', 'oauth token')

    subscribe = client.channels.check_subscription_by_user(channel_id, user_id)

    assert len(responses.calls) == 1
    assert isinstance(subscribe, Subscription)
    assert subscribe.id == example_subscription['_id']
    assert isinstance(subscribe.user, User)
    assert subscribe.user.id == example_user['_id']
    assert subscribe.user.name == example_user['name']


@responses.activate
def test_get_videos():
    channel_id = example_channel['_id']
    response = {
        'videos': [example_video]
    }
    responses.add(responses.GET,
                  '%schannels/%s/videos' % (BASE_URL, channel_id),
                  body=json.dumps(response),
                  status=200,
                  content_type='application/json')

    client = TwitchClient('client id', 'oauth token')

    videos = client.channels.get_videos(channel_id)

    assert len(responses.calls) == 1
    assert len(videos) == 1
    assert isinstance(videos[0], Video)
    video = videos[0]
    assert isinstance(video, Video)
    assert video.id == example_video['_id']
    assert video.description == example_video['description']
    assert video.fps['1080p'] == example_video['fps']['1080p']


@responses.activate
@pytest.mark.parametrize('param,value', [
    ('limit', 101),
    ('broadcast_type', 'abcd'),
    ('sort', 'abcd')
])
def test_get_videos_raises_if_wrong_params_are_passed_in(param, value):
    client = TwitchClient('client id', 'oauth token')
    kwargs = {param: value}
    with pytest.raises(TwitchAttributeException):
        client.channels.get_videos('1234', **kwargs)


@responses.activate
def test_start_commercial():
    channel_id = example_channel['_id']
    response = {
        "duration": 30,
        "message": "",
        "retryafter": 480
    }
    responses.add(responses.POST,
                  '%schannels/%s/commercial' % (BASE_URL, channel_id),
                  body=json.dumps(response),
                  status=200,
                  content_type='application/json')

    client = TwitchClient('client id', 'oauth token')

    commercial = client.channels.start_commercial(channel_id)

    assert len(responses.calls) == 1
    assert isinstance(commercial, dict)
    assert commercial['duration'] == response['duration']


@responses.activate
def test_reset_stream_key():
    channel_id = example_channel['_id']
    responses.add(responses.DELETE,
                  '%schannels/%s/stream_key' % (BASE_URL, channel_id),
                  body=json.dumps(example_channel),
                  status=200,
                  content_type='application/json')

    client = TwitchClient('client id', 'oauth token')

    channel = client.channels.reset_stream_key(channel_id)

    assert len(responses.calls) == 1
    assert isinstance(channel, Channel)
    assert channel.id == example_channel['_id']
    assert channel.name == example_channel['name']


@responses.activate
def test_get_community():
    channel_id = example_channel['_id']
    responses.add(responses.GET,
                  '%schannels/%s/community' % (BASE_URL, channel_id),
                  body=json.dumps(example_community),
                  status=200,
                  content_type='application/json')

    client = TwitchClient('client id')

    community = client.channels.get_community(channel_id)

    assert len(responses.calls) == 1
    assert isinstance(community, Community)
    assert community.id == example_community['_id']
    assert community.name == example_community['name']


@responses.activate
def test_set_community():
    channel_id = example_channel['_id']
    community_id = example_community['_id']
    responses.add(responses.PUT,
                  '%schannels/%s/community/%s' % (BASE_URL, channel_id, community_id),
                  status=204,
                  content_type='application/json')

    client = TwitchClient('client id')

    client.channels.set_community(channel_id, community_id)

    assert len(responses.calls) == 1


@responses.activate
def test_delete_from_community():
    channel_id = example_channel['_id']
    responses.add(responses.DELETE,
                  '%schannels/%s/community' % (BASE_URL, channel_id),
                  body=json.dumps(example_community),
                  status=204,
                  content_type='application/json')

    client = TwitchClient('client id')

    client.channels.delete_from_community(channel_id)

    assert len(responses.calls) == 1
