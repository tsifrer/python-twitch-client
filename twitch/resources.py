import six


def convert_to_twitch_object(name, data):
    types = {
        'channel': Channel,
        'videos': Video,
        'user': User,
        'game': Game
    }

    if isinstance(data, list):
        return [convert_to_twitch_object(name, x) for x in data]
    elif isinstance(data, dict) and name in types:
        obj = types.get(name)
        return obj.construct_from(data)

    return data


class TwitchObject(dict):

    def __setattr__(self, name, value):
        if name[0] == '_' or name in self.__dict__:
            return super(TwitchObject, self).__setattr__(name, value)

        self[name] = value

    def __getattr__(self, name):
        if name[0] == '_' or name in self.__dict__:
            return super(TwitchObject, self).__getattr__(name)

        return self[name]

    def __delattr__(self, name):
        if name[0] == '_':
            super(TwitchObject, self).__delattr__(name)

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


class User(TwitchObject):
    pass


class Follow(TwitchObject):
    pass


class Subscription(TwitchObject):
    pass


class UserBlock(TwitchObject):
    pass


class TopGame(TwitchObject):
    pass


class Game(TwitchObject):
    pass


class Video(TwitchObject):
    pass


class Channel(TwitchObject):
    pass


class Team(TwitchObject):
    pass


class Community(TwitchObject):
    pass


class Ingest(TwitchObject):
    pass


class Stream(TwitchObject):
    pass


class Featured(TwitchObject):
    pass
