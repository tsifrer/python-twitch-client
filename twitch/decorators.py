from twitch.exceptions import TwitchException


def oauth_required(func):
    def wrapper(*args, **kwargs):
        if not args[0]._oauth_token:
            raise TwitchException('OAuth token required')
        return func(*args, **kwargs)
    return wrapper
