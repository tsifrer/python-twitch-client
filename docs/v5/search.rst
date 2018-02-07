Search
======

.. currentmodule:: twitch.api.search

.. class:: Search()

    This class provides methods for easy access to `Twitch Search API`_.

    .. classmethod:: channels(query, limit, offset)

        Searches for channels based on a specified query parameter.

        :param string query: Search query
        :param int limit: Maximum number of objects to return. Default 25. Maximum 100.
        :param int offset: Object offset for pagination of result. Default 0.

        .. code-block:: python

            >>> from twitch import TwitchClient
            >>> client = TwitchClient('<my client id>')
            >>> channels = client.search.channels('lirik', limit=69, offset=420)


    .. classmethod:: games(query, live)

        Searches for games based on a specified query parameter.

        :param string query: Search query
        :param boolean live: If `True`, returns only games that are live on at least one channel.
               Default: `False`.

    .. classmethod:: streams(query, limit, offset, hls)

        Searches for streams based on a specified query parameter.

        :param string query: Search query
        :param int limit: Maximum number of objects to return. Default 25. Maximum 100.
        :param int offset: Object offset for pagination of result. Default 0.
        :param boolean hls: If `True`, returns only HLS streams; if `False`, only RTMP streams;
               if `None`, both HLS and RTMP streams. 



.. _`Twitch Search API`: https://dev.twitch.tv/docs/v5/reference/search/
