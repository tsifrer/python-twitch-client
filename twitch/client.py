
class TwitchClient(object):

    def __init__(self, client_id=None, oauth_token=None):
        self._client_id = client_id
        self._oauth_token = oauth_token

        self._channels = None
        self._chat = None
        self._communities = None
        self._ingests = None
        self._users = None
        self._games = None
        self._teams = None
        self._streams = None
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

    @property
    def channels(self):
        from .api.channels import Channels
        if not self._channels:
            self._channels = Channels(
                client_id=self._client_id, oauth_token=self._oauth_token)
        return self._channels

    @property
    def ingests(self):
        from .api.ingests import Ingests
        if not self._ingests:
            self._ingests = Ingests(
                client_id=self._client_id, oauth_token=self._oauth_token)
        return self._ingests

    @property
    def streams(self):
        from .api.streams import Streams
        if not self._streams:
            self._streams = Streams(
                client_id=self._client_id, oauth_token=self._oauth_token)
        return self._streams

    @property
    def teams(self):
        from .api.teams import Teams
        if not self._teams:
            self._teams = Teams(
                client_id=self._client_id, oauth_token=self._oauth_token)
        return self._teams

    @property
    def chat(self):
        from .api.chat import Chat
        if not self._chat:
            self._chat = Chat(
                client_id=self._client_id, oauth_token=self._oauth_token)
        return self._chat

    @property
    def communities(self):
        from .api.communities import Communities
        if not self._communities:
            self._communities = Communities(
                client_id=self._client_id, oauth_token=self._oauth_token)
        return self._communities
