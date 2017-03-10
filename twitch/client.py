from .api import (
    ChannelFeed, Channels, Chat, Collections, Communities, Games, Ingests, Search, Streams, Teams,
    Users, Videos
)


class TwitchClient(object):
    def __init__(self, client_id=None, oauth_token=None):
        self._client_id = client_id
        self._oauth_token = oauth_token

        self._channel_feed = None
        self._channels = None
        self._chat = None
        self._collections = None
        self._communities = None
        self._games = None
        self._ingests = None
        self._search = None
        self._streams = None
        self._teams = None
        self._users = None
        self._videos = None

    @property
    def channel_feed(self):
        if not self._channel_feed:
            self._channel_feed = ChannelFeed(
                client_id=self._client_id, oauth_token=self._oauth_token)
        return self._channel_feed

    @property
    def channels(self):
        if not self._channels:
            self._channels = Channels(
                client_id=self._client_id, oauth_token=self._oauth_token)
        return self._channels

    @property
    def chat(self):
        if not self._chat:
            self._chat = Chat(
                client_id=self._client_id, oauth_token=self._oauth_token)
        return self._chat

    @property
    def collections(self):
        if not self._collections:
            self._collections = Collections(
                client_id=self._client_id, oauth_token=self._oauth_token)
        return self._collections

    @property
    def communities(self):
        if not self._communities:
            self._communities = Communities(
                client_id=self._client_id, oauth_token=self._oauth_token)
        return self._communities

    @property
    def games(self):
        if not self._games:
            self._games = Games(
                client_id=self._client_id, oauth_token=self._oauth_token)
        return self._games

    @property
    def ingests(self):
        if not self._ingests:
            self._ingests = Ingests(
                client_id=self._client_id, oauth_token=self._oauth_token)
        return self._ingests

    @property
    def search(self):
        if not self._search:
            self._search = Search(
                client_id=self._client_id, oauth_token=self._oauth_token)
        return self._search

    @property
    def streams(self):
        if not self._streams:
            self._streams = Streams(
                client_id=self._client_id, oauth_token=self._oauth_token)
        return self._streams

    @property
    def teams(self):
        if not self._teams:
            self._teams = Teams(
                client_id=self._client_id, oauth_token=self._oauth_token)
        return self._teams

    @property
    def users(self):
        if not self._users:
            self._users = Users(
                client_id=self._client_id, oauth_token=self._oauth_token)
        return self._users

    @property
    def videos(self):
        if not self._videos:
            self._videos = Videos(
                client_id=self._client_id, oauth_token=self._oauth_token)
        return self._videos
