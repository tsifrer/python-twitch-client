import json

import responses

from twitch.client import TwitchClient
from twitch.constants import BASE_URL
from twitch.resources import Channel, Follow, Subscription, User, UserBlock


example_user = {
    '_id': '44322889',
    'name': 'dallas',
}

example_channel = {
    '_id': 121059319,
    'name': 'moonmoon_ow',
}

example_follow = {
    'created_at': '2016-09-16T20:37:39Z',
    'notifications': False,
    'channel': example_channel
}

example_block = {
    '_id': 34105660,
    'updated_at': '2016-12-15T18:58:11Z',
    'user': example_user
}


@responses.activate
def test_get():
    responses.add(responses.GET,
                  '%suser' % BASE_URL,
                  body=json.dumps(example_user),
                  status=200,
                  content_type='application/json')

    client = TwitchClient('client id', 'oauth token')

    user = client.users.get()

    assert len(responses.calls) == 1
    assert isinstance(user, User)
    assert user.id == example_user['_id']
    assert user.name == example_user['name']


@responses.activate
def test_get_by_id():
    user_id = 1234
    responses.add(responses.GET,
                  '%susers/%s' % (BASE_URL, user_id),
                  body=json.dumps(example_user),
                  status=200,
                  content_type='application/json')

    client = TwitchClient('client id')

    user = client.users.get_by_id(user_id)

    assert len(responses.calls) == 1
    assert isinstance(user, User)
    assert user.id == example_user['_id']
    assert user.name == example_user['name']


@responses.activate
def test_get_emotes():
    user_id = 1234
    response = {
        'emoticon_sets': {
            '17937': [
                {
                    'code': 'Kappa',
                    'id': 25
                },
            ],
        }
    }
    responses.add(responses.GET,
                  '%susers/%s/emotes' % (BASE_URL, user_id),
                  body=json.dumps(response),
                  status=200,
                  content_type='application/json')

    client = TwitchClient('client id', 'oauth token')

    emotes = client.users.get_emotes(user_id)

    assert len(responses.calls) == 1
    assert isinstance(emotes, dict)
    assert emotes['17937'] == response['emoticon_sets']['17937']


@responses.activate
def test_check_subscribed_to_channel():
    user_id = 1234
    channel_id = 12345
    response = {
       '_id': 'c660cb408bc3b542f5bdbba52f3e638e652756b4',
       'created_at': '2016-12-12T15:52:52Z',
       'channel': example_channel,
    }
    responses.add(responses.GET,
                  '%susers/%s/subscriptions/%s' % (BASE_URL, user_id, channel_id),
                  body=json.dumps(response),
                  status=200,
                  content_type='application/json')

    client = TwitchClient('client id', 'oauth token')

    subscription = client.users.check_subscribed_to_channel(user_id, channel_id)

    assert len(responses.calls) == 1
    assert isinstance(subscription, Subscription)
    assert subscription.id == response['_id']
    assert isinstance(subscription.channel, Channel)
    assert subscription.channel.id == example_channel['_id']
    assert subscription.channel.name == example_channel['name']


@responses.activate
def test_get_follows():
    user_id = 1234
    response = {
        '_total': 27,
        'follows': [example_follow]
    }
    responses.add(responses.GET,
                  '%susers/%s/follows/channels' % (BASE_URL, user_id),
                  body=json.dumps(response),
                  status=200,
                  content_type='application/json')

    client = TwitchClient('client id')

    follows = client.users.get_follows(user_id)

    assert len(responses.calls) == 1
    assert len(follows) == 1
    follow = follows[0]
    assert isinstance(follow, Follow)
    assert follow.notifications == example_follow['notifications']
    assert isinstance(follow.channel, Channel)
    assert follow.channel.id == example_channel['_id']
    assert follow.channel.name == example_channel['name']


@responses.activate
def test_check_follows_channel():
    user_id = 1234
    channel_id = 12345
    responses.add(responses.GET,
                  '%susers/%s/follows/channels/%s' % (BASE_URL, user_id, channel_id),
                  body=json.dumps(example_follow),
                  status=200,
                  content_type='application/json')

    client = TwitchClient('client id')

    follow = client.users.check_follows_channel(user_id, channel_id)

    assert len(responses.calls) == 1
    assert isinstance(follow, Follow)
    assert follow.notifications == example_follow['notifications']
    assert isinstance(follow.channel, Channel)
    assert follow.channel.id == example_channel['_id']
    assert follow.channel.name == example_channel['name']


@responses.activate
def test_follow_channel():
    user_id = 1234
    channel_id = 12345
    responses.add(responses.PUT,
                  '%susers/%s/follows/channels/%s' % (BASE_URL, user_id, channel_id),
                  body=json.dumps(example_follow),
                  status=200,
                  content_type='application/json')

    client = TwitchClient('client id', 'oauth token')

    follow = client.users.follow_channel(user_id, channel_id)

    assert len(responses.calls) == 1
    assert isinstance(follow, Follow)
    assert follow.notifications == example_follow['notifications']
    assert isinstance(follow.channel, Channel)
    assert follow.channel.id == example_channel['_id']
    assert follow.channel.name == example_channel['name']


@responses.activate
def test_unfollow_channel():
    user_id = 1234
    channel_id = 12345
    responses.add(responses.DELETE,
                  '%susers/%s/follows/channels/%s' % (BASE_URL, user_id, channel_id),
                  status=204,
                  content_type='application/json')

    client = TwitchClient('client id', 'oauth token')

    client.users.unfollow_channel(user_id, channel_id)

    assert len(responses.calls) == 1


@responses.activate
def test_get_user_block_list():
    user_id = 1234
    response = {
        '_total': 4,
        'blocks': [example_block]
    }
    responses.add(responses.GET,
                  '%susers/%s/blocks' % (BASE_URL, user_id),
                  body=json.dumps(response),
                  status=200,
                  content_type='application/json')

    client = TwitchClient('client id', 'oauth token')

    block_list = client.users.get_user_block_list(user_id)

    assert len(responses.calls) == 1
    assert len(block_list) == 1
    block = block_list[0]
    assert isinstance(block, UserBlock)
    assert block.id == example_block['_id']
    assert isinstance(block.user, User)
    assert block.user.id == example_user['_id']
    assert block.user.name == example_user['name']


@responses.activate
def test_block_user():
    user_id = 1234
    blocked_user_id = 12345
    responses.add(responses.PUT,
                  '%susers/%s/blocks/%s' % (BASE_URL, user_id, blocked_user_id),
                  body=json.dumps(example_block),
                  status=200,
                  content_type='application/json')

    client = TwitchClient('client id', 'oauth token')

    block = client.users.block_user(user_id, blocked_user_id)

    assert len(responses.calls) == 1
    assert isinstance(block, UserBlock)
    assert block.id == example_block['_id']
    assert isinstance(block.user, User)
    assert block.user.id == example_user['_id']
    assert block.user.name == example_user['name']


@responses.activate
def test_unblock_user():
    user_id = 1234
    blocked_user_id = 12345
    responses.add(responses.DELETE,
                  '%susers/%s/blocks/%s' % (BASE_URL, user_id, blocked_user_id),
                  body=json.dumps(example_block),
                  status=200,
                  content_type='application/json')

    client = TwitchClient('client id', 'oauth token')

    client.users.unblock_user(user_id, blocked_user_id)

    assert len(responses.calls) == 1


@responses.activate
def test_translate_usernames_to_ids():
    response = {
        'users': [example_user]
    }
    responses.add(responses.GET,
                  '%susers' % (BASE_URL),
                  body=json.dumps(response),
                  status=200,
                  content_type='application/json')

    client = TwitchClient('client id', 'oauth token')

    users = client.users.translate_usernames_to_ids(['lirik'])

    assert len(responses.calls) == 1
    assert len(users) == 1
    user = users[0]
    assert isinstance(user, User)
    assert user.id == example_user['_id']
    assert user.name == example_user['name']
