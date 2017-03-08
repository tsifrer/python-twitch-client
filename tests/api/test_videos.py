import json

import pytest

import responses

from twitch.client import TwitchClient
from twitch.constants import BASE_URL
from twitch.exceptions import TwitchAttributeException
from twitch.resources import Video


example_video_response = {
   '_id': 'v106400740',
   'description': 'Protect your chat with AutoMod!',
   'fps': {
      '1080p': 23.9767661758746,
   },
}

example_top_response = {
    'vods': [example_video_response]
}

example_followed_response = {
    'videos': [example_video_response]
}


@responses.activate
def test_get_by_id():
    video_id = 'v106400740'
    responses.add(responses.GET,
                  '%svideos/%s' % (BASE_URL, video_id),
                  body=json.dumps(example_video_response),
                  status=200,
                  content_type='application/json')

    client = TwitchClient('client id')

    video = client.videos.get_by_id(video_id)

    assert len(responses.calls) == 1
    assert isinstance(video, Video)
    assert video.id == example_video_response['_id']
    assert video.description == example_video_response['description']
    assert video.fps['1080p'] == example_video_response['fps']['1080p']


@responses.activate
def test_get_top():
    responses.add(responses.GET,
                  '%svideos/top' % BASE_URL,
                  body=json.dumps(example_top_response),
                  status=200,
                  content_type='application/json')

    client = TwitchClient('client id')

    videos = client.videos.get_top()

    assert len(responses.calls) == 1
    assert len(videos) == 1
    assert isinstance(videos[0], Video)
    video = videos[0]
    assert isinstance(video, Video)
    assert video.id == example_video_response['_id']
    assert video.description == example_video_response['description']
    assert video.fps['1080p'] == example_video_response['fps']['1080p']


@responses.activate
@pytest.mark.parametrize('param,value', [
    ('limit', 101),
    ('period', 'abcd'),
    ('broadcast_type', 'abcd'),
])
def test_get_top_raises_if_wrong_params_are_passed_in(param, value):
    client = TwitchClient('client id')
    kwargs = {param: value}
    with pytest.raises(TwitchAttributeException):
        client.videos.get_top(**kwargs)


@responses.activate
def test_get_followed_videos():
    responses.add(responses.GET,
                  '%svideos/followed' % BASE_URL,
                  body=json.dumps(example_followed_response),
                  status=200,
                  content_type='application/json')

    client = TwitchClient('client id', 'oauth token')

    videos = client.videos.get_followed_videos()

    assert len(responses.calls) == 1
    assert len(videos) == 1
    assert isinstance(videos[0], Video)
    video = videos[0]
    assert isinstance(video, Video)
    assert video.id == example_video_response['_id']
    assert video.description == example_video_response['description']
    assert video.fps['1080p'] == example_video_response['fps']['1080p']


@responses.activate
@pytest.mark.parametrize('param,value', [
    ('limit', 101),
    ('broadcast_type', 'abcd'),
])
def test_get_followed_videos_raises_if_wrong_params_are_passed_in(param, value):
    client = TwitchClient('client id', 'oauth token')
    kwargs = {param: value}
    with pytest.raises(TwitchAttributeException):
        client.videos.get_followed_videos(**kwargs)
