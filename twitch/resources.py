from datetime import datetime

import six


def convert_to_twitch_object(name, data):
    types = {
        'channel': Channel,
        'videos': Video,
        'user': User,
        'game': Game,
        'stream': Stream,
        'comments': Comment,
        'owner': User,
    }

    special_types = {
        'created_at': _DateTime,
        'updated_at': _DateTime,
        'published_at': _DateTime,
    }

    if isinstance(data, list):
        return [convert_to_twitch_object(name, x) for x in data]

    if name in special_types:
        obj = special_types.get(name)
        return obj.construct_from(data)

    if isinstance(data, dict) and name in types:
        obj = types.get(name)
        return obj.construct_from(data)

    return data


class TwitchObject(dict):

    def __setattr__(self, name, value):
        if name[0] == '_' or name in self.__dict__:
            return super(TwitchObject, self).__setattr__(name, value)

        self[name] = value

    def __getattr__(self, name):
        return self[name]

    def __delattr__(self, name):
        if name[0] == '_':
            return super(TwitchObject, self).__delattr__(name)

        del self[name]

    def __setitem__(self, key, value):
        key = key.lstrip('_')
        super(TwitchObject, self).__setitem__(key, value)

    @classmethod
    def construct_from(cls, values):
        instance = cls()
        instance.refresh_from(values)
        return instance

    def refresh_from(self, values):
        for key, value in six.iteritems(values.copy()):
            self.__setitem__(key, convert_to_twitch_object(key, value))


class _DateTime(object):

    def construct_from(value):
        try:
            dt = datetime.strptime(value, '%Y-%m-%dT%H:%M:%SZ')
        except ValueError:
            dt = datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%fZ')

        return dt


class Channel(TwitchObject):
    pass


class Collection(TwitchObject):
    pass


class Comment(TwitchObject):
    pass


class Community(TwitchObject):
    pass


class Featured(TwitchObject):
    pass


class Follow(TwitchObject):
    pass


class Game(TwitchObject):
    pass


class Ingest(TwitchObject):
    pass


class Item(TwitchObject):
    pass


class Post(TwitchObject):
    pass


class Stream(TwitchObject):
    pass


class Subscription(TwitchObject):
    pass


class Team(TwitchObject):
    pass


class TopGame(TwitchObject):
    pass


class User(TwitchObject):
    pass


class UserBlock(TwitchObject):
    pass


class Video(TwitchObject):
    pass
