import json

import pytest

import responses

from twitch.client import TwitchClient
from twitch.constants import BASE_URL
from twitch.exceptions import TwitchAttributeException
from twitch.resources import Community, User


example_community = {
   '_id': 'e9f17055-810f-4736-ba40-fba4ac541caa',
   'name': 'DallasTesterCommunity',
}

example_user = {
    '_id': '44322889',
    'name': 'dallas',
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


@responses.activate
def test_get_top():
    response = {
        '_cursor': 'MTA=',
        '_total': 100,
        'communities': [example_community]
    }

    responses.add(responses.GET,
                  '%scommunities/top' % BASE_URL,
                  body=json.dumps(response),
                  status=200,
                  content_type='application/json')

    client = TwitchClient('client id')

    communities = client.communities.get_top()

    assert len(responses.calls) == 1
    assert len(communities) == 1
    community = communities[0]
    assert isinstance(community, Community)
    assert community.id == example_community['_id']
    assert community.name == example_community['name']


@responses.activate
@pytest.mark.parametrize('param,value', [
    ('limit', 101),
])
def test_get_top_raises_if_wrong_params_are_passed_in(param, value):
    client = TwitchClient('client id')
    kwargs = {param: value}
    with pytest.raises(TwitchAttributeException):
        client.communities.get_top(**kwargs)


@responses.activate
def test_get_banned_users():
    community_id = 'abcd'
    response = {
        '_cursor': '',
        'banned_users': [example_user]
    }

    responses.add(responses.GET,
                  '%scommunities/%s/bans' % (BASE_URL, community_id),
                  body=json.dumps(response),
                  status=200,
                  content_type='application/json')

    client = TwitchClient('client id', 'oauth token')

    users = client.communities.get_banned_users(community_id)

    assert len(responses.calls) == 1
    assert len(users) == 1
    user = users[0]
    assert isinstance(user, User)
    assert user.id == example_user['_id']
    assert user.name == example_user['name']


@responses.activate
@pytest.mark.parametrize('param,value', [
    ('limit', 101),
])
def test_get_banned_users_raises_if_wrong_params_are_passed_in(param, value):
    client = TwitchClient('client id', 'oauth token')
    kwargs = {param: value}
    with pytest.raises(TwitchAttributeException):
        client.communities.get_banned_users('1234', **kwargs)


@responses.activate
def test_ban_user():
    community_id = 'abcd'
    user_id = 1234
    responses.add(responses.PUT,
                  '%scommunities/%s/bans/%s' % (BASE_URL, community_id, user_id),
                  status=204,
                  content_type='application/json')

    client = TwitchClient('client id', 'oauth token')

    client.communities.ban_user(community_id, user_id)

    assert len(responses.calls) == 1


@responses.activate
def test_unban_user():
    community_id = 'abcd'
    user_id = 1234
    responses.add(responses.DELETE,
                  '%scommunities/%s/bans/%s' % (BASE_URL, community_id, user_id),
                  status=204,
                  content_type='application/json')

    client = TwitchClient('client id', 'oauth token')

    client.communities.unban_user(community_id, user_id)

    assert len(responses.calls) == 1


@responses.activate
def test_create_avatar_image():
    community_id = 'abcd'
    responses.add(responses.POST,
                  '%scommunities/%s/images/avatar' % (BASE_URL, community_id),
                  status=204,
                  content_type='application/json')

    client = TwitchClient('client id', 'oauth token')

    client.communities.create_avatar_image(community_id, 'imagecontent')

    assert len(responses.calls) == 1


@responses.activate
def test_delete_avatar_image():
    community_id = 'abcd'
    responses.add(responses.DELETE,
                  '%scommunities/%s/images/avatar' % (BASE_URL, community_id),
                  status=204,
                  content_type='application/json')

    client = TwitchClient('client id', 'oauth token')

    client.communities.delete_avatar_image(community_id)

    assert len(responses.calls) == 1


@responses.activate
def test_create_cover_image():
    community_id = 'abcd'
    responses.add(responses.POST,
                  '%scommunities/%s/images/cover' % (BASE_URL, community_id),
                  status=204,
                  content_type='application/json')

    client = TwitchClient('client id', 'oauth token')

    client.communities.create_cover_image(community_id, 'imagecontent')

    assert len(responses.calls) == 1


@responses.activate
def test_delete_cover_image():
    community_id = 'abcd'
    responses.add(responses.DELETE,
                  '%scommunities/%s/images/cover' % (BASE_URL, community_id),
                  status=204,
                  content_type='application/json')

    client = TwitchClient('client id', 'oauth token')

    client.communities.delete_cover_image(community_id)

    assert len(responses.calls) == 1


@responses.activate
def test_get_moderators():
    community_id = 'abcd'
    response = {
        'moderators': [example_user]
    }

    responses.add(responses.GET,
                  '%scommunities/%s/moderators' % (BASE_URL, community_id),
                  body=json.dumps(response),
                  status=200,
                  content_type='application/json')

    client = TwitchClient('client id', 'oauth token')

    moderators = client.communities.get_moderators(community_id)

    assert len(responses.calls) == 1
    assert len(moderators) == 1
    user = moderators[0]
    assert isinstance(user, User)
    assert user.id == example_user['_id']
    assert user.name == example_user['name']


@responses.activate
def test_add_moderator():
    community_id = 'abcd'
    user_id = 12345
    responses.add(responses.PUT,
                  '%scommunities/%s/moderators/%s' % (BASE_URL, community_id, user_id),
                  status=204,
                  content_type='application/json')

    client = TwitchClient('client id', 'oauth token')

    client.communities.add_moderator(community_id, user_id)

    assert len(responses.calls) == 1


@responses.activate
def test_delete_moderator():
    community_id = 'abcd'
    user_id = 12345
    responses.add(responses.DELETE,
                  '%scommunities/%s/moderators/%s' % (BASE_URL, community_id, user_id),
                  status=204,
                  content_type='application/json')

    client = TwitchClient('client id', 'oauth token')

    client.communities.delete_moderator(community_id, user_id)

    assert len(responses.calls) == 1


@responses.activate
def test_get_permissions():
    community_id = 'abcd'
    response = {
        'ban': True,
        'timeout': True,
        'edit': True
    }

    responses.add(responses.GET,
                  '%scommunities/%s/permissions' % (BASE_URL, community_id),
                  body=json.dumps(response),
                  status=200,
                  content_type='application/json')

    client = TwitchClient('client id', 'oauth token')

    permissions = client.communities.get_permissions(community_id)

    assert len(responses.calls) == 1
    assert isinstance(permissions, dict)
    assert permissions['ban'] is True


@responses.activate
def test_report_violation():
    community_id = 'abcd'
    responses.add(responses.POST,
                  '%scommunities/%s/report_channel' % (BASE_URL, community_id),
                  status=204,
                  content_type='application/json')

    client = TwitchClient('client id', 'oauth token')

    client.communities.report_violation(community_id, 12345)

    assert len(responses.calls) == 1


@responses.activate
def test_get_timed_out_users():
    community_id = 'abcd'
    response = {
        '_cursor': '',
        'timed_out_users': [example_user]
    }

    responses.add(responses.GET,
                  '%scommunities/%s/timeouts' % (BASE_URL, community_id),
                  body=json.dumps(response),
                  status=200,
                  content_type='application/json')

    client = TwitchClient('client id', 'oauth token')

    users = client.communities.get_timed_out_users(community_id)

    assert len(responses.calls) == 1
    assert len(users) == 1
    user = users[0]
    assert isinstance(user, User)
    assert user.id == example_user['_id']
    assert user.name == example_user['name']


@responses.activate
@pytest.mark.parametrize('param,value', [
    ('limit', 101),
])
def test_get_timed_out_users_raises_if_wrong_params_are_passed_in(param, value):
    client = TwitchClient('client id', 'oauth token')
    kwargs = {param: value}
    with pytest.raises(TwitchAttributeException):
        client.communities.get_timed_out_users('1234', **kwargs)


@responses.activate
def test_add_timed_out_user():
    community_id = 'abcd'
    user_id = 12345
    responses.add(responses.PUT,
                  '%scommunities/%s/timeouts/%s' % (BASE_URL, community_id, user_id),
                  status=204,
                  content_type='application/json')

    client = TwitchClient('client id', 'oauth token')

    client.communities.add_timed_out_user(community_id, user_id, 5)

    assert len(responses.calls) == 1


@responses.activate
def test_delete_timed_out_user():
    community_id = 'abcd'
    user_id = 12345
    responses.add(responses.DELETE,
                  '%scommunities/%s/timeouts/%s' % (BASE_URL, community_id, user_id),
                  status=204,
                  content_type='application/json')

    client = TwitchClient('client id', 'oauth token')

    client.communities.delete_timed_out_user(community_id, user_id)

    assert len(responses.calls) == 1
