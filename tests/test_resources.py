from datetime import datetime

import pytest

from twitch.resources import (
    Channel, Comment, Community, Featured, Follow, Game, Ingest, Stream, StreamMetadata,
    Subscription, Team, TopGame, TwitchObject, User, UserBlock, Video, convert_to_twitch_object
)


def test_convert_to_twitch_object_output_returns_string_for_string_input():
    data = 'squarepants'
    result = convert_to_twitch_object('spongebob', data)
    assert result == data


def test_convert_to_twitch_object_output_returns_list_for_list_input():
    data = ['squarepants', 'patrick', 'star']
    result = convert_to_twitch_object('spongebob', data)
    assert isinstance(result, list)


def test_convert_to_twitch_object_output_returns_list_of_objects_for_list_of_objects_input():
    data = [{'spongebob': 'squarepants'}, {'patrick': 'star'}]
    result = convert_to_twitch_object('channel', data)
    assert isinstance(result, list)
    assert isinstance(result[0], Channel)
    assert result[0] == data[0]


@pytest.mark.parametrize('name,data,expected_type', [
    ('channel', {'spongebob': 'squarepants'}, Channel),
    ('videos', {'spongebob': 'squarepants'}, Video),
    ('user', {'spongebob': 'squarepants'}, User),
    ('game', {'spongebob': 'squarepants'}, Game),
    ('stream', {'spongebob': 'squarepants'}, Stream),
    ('comments', {'spongebob': 'squarepants'}, Comment),
    ('owner', {'spongebob': 'squarepants'}, User),
])
def test_convert_to_twitch_object_output_returns_correct_object(name, data, expected_type):
    result = convert_to_twitch_object(name, data)
    assert isinstance(result, expected_type)
    assert result == data


@pytest.mark.parametrize('name,data,expected', [
    ('created_at', '2016-11-29T15:52:27Z', datetime(2016, 11, 29, 15, 52, 27)),
    ('updated_at', '2017-03-06T18:40:51.855Z', datetime(2017, 3, 6, 18, 40, 51, 855000)),
    ('published_at', '2017-02-14T22:27:54Z', datetime(2017, 2, 14, 22, 27, 54)),
])
def test_datetimes_are_converted_correctly_to_datetime_objects(name, data, expected):
    result = convert_to_twitch_object(name, data)
    assert isinstance(result, datetime)
    assert result == expected


class TestTwitchObject(object):

    def test_attributes_are_stored_and_fetched_from_dict(self):
        obj = TwitchObject()
        value = 'spongebob'
        obj.spongebob = value

        assert 'spongebob' in obj
        assert '_spongebob' not in obj.__dict__
        assert 'spongebob' not in obj.__dict__
        assert obj['spongebob'] == value
        assert obj.spongebob == value

        del obj.spongebob

        assert 'spongebob' not in obj
        assert 'spongebob' not in obj.__dict__

    def test_prefixed_attributes_are_stored_on_the_object(self):
        obj = TwitchObject()
        value = 'spongebob'
        obj._spongebob = value

        obj._spongebob
        getattr(obj, '_spongebob')
        assert 'spongebob' not in obj
        assert '_spongebob' not in obj
        assert '_spongebob' in obj.__dict__
        assert obj._spongebob == value

        del obj._spongebob

        assert 'spongebob' not in obj
        assert 'spongebob' not in obj.__dict__

    def test_setitem_sets_item_to_dict(self):
        obj = TwitchObject()
        value = 'squarepants'
        obj['spongebob'] = value
        assert obj['spongebob'] == value

    def test_setitem_removes_underscore_prefix(self):
        obj = TwitchObject()
        value = 'squarepants'
        obj['_spongebob'] = value
        assert obj['spongebob'] == value
        assert '_spongebob' not in obj
        assert '_spongebob' not in obj.__dict__

    def test_construct_form_returns_class_with_set_values(self):
        obj = TwitchObject.construct_from({'spongebob': 'squarepants'})
        assert isinstance(obj, TwitchObject)
        assert obj.spongebob == 'squarepants'

    def test_refresh_from_sets_all_values_to_object(self):
        obj = TwitchObject()
        obj.refresh_from({'spongebob': 'squarepants', 'patrick': 'star', '_id': 1234})

        assert obj.spongebob == 'squarepants'
        assert obj['patrick'] == 'star'
        assert obj.id == 1234


@pytest.mark.parametrize('resource', [
    (Channel),
    (Community),
    (Featured),
    (Follow),
    (Game),
    (Ingest),
    (Stream),
    (StreamMetadata),
    (Subscription),
    (Team),
    (TopGame),
    (User),
    (UserBlock),
    (Video),
])
def test_resource_gets_created_correctly(resource):
    obj = resource.construct_from({'spongebob': 'squarepants', '_id': 1234})
    assert isinstance(obj, resource)
    assert obj.id == 1234
    assert obj.spongebob == 'squarepants'
