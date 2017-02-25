
def oauth_required(func):
    def wrapper(*args):
        assert args[0]._oauth_token, 'OAuth token required'
        return func(*args)
    return wrapper
