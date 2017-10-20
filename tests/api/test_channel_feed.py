import json

import pytest

import responses

from twitch.client import TwitchClient
from twitch.constants import BASE_URL
from twitch.exceptions import TwitchAttributeException
from twitch.resources import Comment, Post

# Note: comment doesn't have id prefixed with _ for some reason
example_comment = {
    'id': '132629',
    'body': 'Hey there! KappaHD',
    'created_at': '2016-11-29T15:52:27Z',
}

# Note: post doesn't have id prefixed with _ for some reason
example_post = {
    'id': '443228891479487861',
    'body': 'News feed post!',
    'comments': {
        '_cursor': '1480434747093939000',
        '_total': 1,
        'comments': [example_comment]
    },
    'created_at': '2016-11-18T16:51:01Z',
}


@responses.activate
def test_get_posts():
    channel_id = '1234'
    response = {
        '_cursor': '1479487861147094000',
        '_topic': 'feeds.channel.44322889',
        'posts': [example_post]
    }
    responses.add(responses.GET,
                  '%sfeed/%s/posts' % (BASE_URL, channel_id),
                  body=json.dumps(response),
                  status=200,
                  content_type='application/json')

    client = TwitchClient('client id')

    posts = client.channel_feed.get_posts(channel_id)

    assert len(responses.calls) == 1
    assert len(posts) == 1
    post = posts[0]
    assert isinstance(post, Post)
    assert post.id == example_post['id']
    assert post.body == example_post['body']


@responses.activate
@pytest.mark.parametrize('param,value', [
    ('limit', 101),
    ('comments', 6),
])
def test_get_posts_raises_if_wrong_params_are_passed_in(param, value):
    client = TwitchClient('client id')
    kwargs = {param: value}
    with pytest.raises(TwitchAttributeException):
        client.channel_feed.get_posts('1234', **kwargs)


@responses.activate
def test_get_post():
    channel_id = '1234'
    post_id = example_post['id']
    responses.add(responses.GET,
                  '%sfeed/%s/posts/%s' % (BASE_URL, channel_id, post_id),
                  body=json.dumps(example_post),
                  status=200,
                  content_type='application/json')

    client = TwitchClient('client id')

    post = client.channel_feed.get_post(channel_id, post_id)

    assert len(responses.calls) == 1
    assert isinstance(post, Post)
    assert post.id == example_post['id']
    assert post.body == example_post['body']


@responses.activate
@pytest.mark.parametrize('param,value', [
    ('comments', 6),
])
def test_get_post_raises_if_wrong_params_are_passed_in(param, value):
    client = TwitchClient('client id')
    kwargs = {param: value}
    with pytest.raises(TwitchAttributeException):
        client.channel_feed.get_post('1234', example_post['id'], **kwargs)


@responses.activate
def test_create_post():
    channel_id = '1234'
    response = {
        'post': example_post,
        'tweet': None
    }
    responses.add(responses.POST,
                  '%sfeed/%s/posts' % (BASE_URL, channel_id),
                  body=json.dumps(response),
                  status=200,
                  content_type='application/json')

    client = TwitchClient('client id', 'oauth token')

    post = client.channel_feed.create_post(channel_id, 'abcd')

    assert len(responses.calls) == 1
    assert isinstance(post, Post)
    assert post.id == example_post['id']
    assert post.body == example_post['body']


@responses.activate
def test_delete_post():
    channel_id = '1234'
    post_id = example_post['id']
    responses.add(responses.DELETE,
                  '%sfeed/%s/posts/%s' % (BASE_URL, channel_id, post_id),
                  body=json.dumps(example_post),
                  status=200,
                  content_type='application/json')

    client = TwitchClient('client id', 'oauth token')

    post = client.channel_feed.delete_post(channel_id, post_id)

    assert len(responses.calls) == 1
    assert isinstance(post, Post)
    assert post.id == example_post['id']


@responses.activate
def test_create_reaction_to_post():
    channel_id = '1234'
    post_id = example_post['id']
    response = {
        'id': '24989127',
        'emote_id': '25',
        'user': {},
        'created_at': '2016-11-29T15:51:12Z',
    }
    responses.add(responses.POST,
                  '%sfeed/%s/posts/%s/reactions' % (BASE_URL, channel_id, post_id),
                  body=json.dumps(response),
                  status=200,
                  content_type='application/json')

    client = TwitchClient('client id', 'oauth token')

    response = client.channel_feed.create_reaction_to_post(
        channel_id, post_id, response['emote_id'])

    assert len(responses.calls) == 1
    assert response['id']


@responses.activate
def test_delete_reaction_to_post():
    channel_id = '1234'
    post_id = example_post['id']
    body = {
        'deleted': True
    }
    responses.add(responses.DELETE,
                  '%sfeed/%s/posts/%s/reactions' % (BASE_URL, channel_id, post_id),
                  body=json.dumps(body),
                  status=200,
                  content_type='application/json')

    client = TwitchClient('client id', 'oauth token')

    response = client.channel_feed.delete_reaction_to_post(channel_id, post_id, '1234')

    assert len(responses.calls) == 1
    assert response['deleted']


@responses.activate
def test_get_post_comments():
    channel_id = '1234'
    post_id = example_post['id']
    response = {
        '_cursor': '1480651694954867000',
        '_total': 1,
        'comments': [example_comment]
    }
    responses.add(responses.GET,
                  '%sfeed/%s/posts/%s/comments' % (BASE_URL, channel_id, post_id),
                  body=json.dumps(response),
                  status=200,
                  content_type='application/json')

    client = TwitchClient('client id')

    comments = client.channel_feed.get_post_comments(channel_id, post_id)

    assert len(responses.calls) == 1
    assert len(comments) == 1
    comment = comments[0]
    assert isinstance(comment, Comment)
    assert comment.id == example_comment['id']
    assert comment.body == example_comment['body']


@responses.activate
@pytest.mark.parametrize('param,value', [
    ('limit', 101),
])
def test_get_post_comments_raises_if_wrong_params_are_passed_in(param, value):
    client = TwitchClient('client id')
    kwargs = {param: value}
    with pytest.raises(TwitchAttributeException):
        client.channel_feed.get_post_comments('1234', example_post['id'], **kwargs)


@responses.activate
def test_create_post_comment():
    channel_id = '1234'
    post_id = example_post['id']
    responses.add(responses.POST,
                  '%sfeed/%s/posts/%s/comments' % (BASE_URL, channel_id, post_id),
                  body=json.dumps(example_comment),
                  status=200,
                  content_type='application/json')

    client = TwitchClient('client id', 'oauth token')

    comment = client.channel_feed.create_post_comment(channel_id, post_id, 'abcd')

    assert len(responses.calls) == 1
    assert isinstance(comment, Comment)
    assert comment.id == example_comment['id']
    assert comment.body == example_comment['body']


@responses.activate
def test_delete_post_comment():
    channel_id = '1234'
    post_id = example_post['id']
    comment_id = example_comment['id']
    responses.add(responses.DELETE,
                  '%sfeed/%s/posts/%s/comments/%s' % (BASE_URL, channel_id, post_id, comment_id),
                  body=json.dumps(example_comment),
                  status=200,
                  content_type='application/json')

    client = TwitchClient('client id', 'oauth token')

    comment = client.channel_feed.delete_post_comment(channel_id, post_id, comment_id)

    assert len(responses.calls) == 1
    assert isinstance(comment, Comment)
    assert comment.id == example_comment['id']


@responses.activate
def test_create_reaction_to_comment():
    channel_id = '1234'
    post_id = example_post['id']
    comment_id = example_comment['id']
    body = {
        'created_at': '2016-12-02T04:26:47Z',
        'emote_id': '1',
        'id': '1341393b-e872-4554-9f6f-acd5f8b669fc',
        'user': {}
    }
    url = '%sfeed/%s/posts/%s/comments/%s/reactions' % (BASE_URL, channel_id, post_id, comment_id)
    responses.add(responses.POST,
                  url,
                  body=json.dumps(body),
                  status=200,
                  content_type='application/json')

    client = TwitchClient('client id', 'oauth token')

    response = client.channel_feed.create_reaction_to_comment(channel_id, post_id, comment_id, '1')

    assert len(responses.calls) == 1
    assert response['id']


@responses.activate
def test_delete_reaction_to_comment():
    channel_id = '1234'
    post_id = example_post['id']
    comment_id = example_comment['id']
    body = {
        'deleted': True
    }
    url = '%sfeed/%s/posts/%s/comments/%s/reactions' % (BASE_URL, channel_id, post_id, comment_id)
    responses.add(responses.DELETE,
                  url,
                  body=json.dumps(body),
                  status=200,
                  content_type='application/json')

    client = TwitchClient('client id', 'oauth token')

    response = client.channel_feed.delete_reaction_to_comment(channel_id, post_id, comment_id, '1')

    assert len(responses.calls) == 1
    assert response['deleted']
