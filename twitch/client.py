
class TwitchClient(object):

    def __init__(self, client_id=None, oauth_token=None):
        self._client_id = client_id
        self._oauth_token = oauth_token

        self._users = None
        self._games = None
        self._videos = None

    @property
    def users(self):
        from .api.users import Users
        if not self._users:
            self._users = Users(
                client_id=self._client_id, oauth_token=self._oauth_token)
        return self._users

    @property
    def games(self):
        from .api.games import Games
        if not self._games:
            self._games = Games(
                client_id=self._client_id, oauth_token=self._oauth_token)
        return self._games

    @property
    def videos(self):
        from .api.videos import Videos
        if not self._videos:
            self._videos = Videos(
                client_id=self._client_id, oauth_token=self._oauth_token)
        return self._videos
