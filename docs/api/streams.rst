Streams
=======

.. currentmodule:: twitch.api.streams

.. class:: Streams()

    This class provides methods for easy access to `Twitch Streams API`_.

    .. classmethod:: get_stream_by_user(channel_id, stream_type)

        Gets stream information for a specified user.

        :param string channel_id: ID of the channel you want to get information of
        :param string stream_type: Constrains the type of streams returned.
                      Default STREAM_TYPE_LIVE.


    .. classmethod:: get_live_streams(channel, game, language, stream_type, limit, offset)

        Gets a list of live streams.

        :param string channel: Comma-separated list of channel IDs you want to get
        :param string game: Game of the streams returned
        :param string language: Constrains the language of the streams returned
        :param string stream_type: Constrains the type of streams returned.
                      Default STREAM_TYPE_LIVE.
        :param int limit: Maximum number of objects to return. Default 25. Maximum 100.
        :param int offset: Object offset for pagination of result. Default 0.


    .. classmethod:: get_summary(game)

        Gets a list of summaries of live streams.

        :param string game: Game of the streams returned


    .. classmethod:: get_featured(limit, offset)

        Gets a list of all featured live streams.

        :param int limit: Maximum number of objects to return. Default 25. Maximum 100.
        :param int offset: Object offset for pagination of result. Default 0.


    .. classmethod:: get_followed(stream_type, limit, offset)

        Gets a list of online streams a user is following, based on a specified OAuth token.

        :param string stream_type: Constrains the type of streams returned.
                      Default STREAM_TYPE_LIVE.
        :param int limit: Maximum number of objects to return. Default 25. Maximum 100.
        :param int offset: Object offset for pagination of result. Default 0.


        .. code-block:: python

            >>> from twitch import TwitchClient
            >>> client = TwitchClient('<my client id>', '<my oauth token>')
            >>> followed = client.streams.get_followed()


.. _`Twitch Streams API`: https://dev.twitch.tv/docs/v5/reference/streams/
