
class TwitchException(Exception):
    pass


class TwitchAuthException(TwitchException):
    pass


class TwitchAttributeException(TwitchException):
    pass


class TwitchNotProvidedException(TwitchException):
    pass
