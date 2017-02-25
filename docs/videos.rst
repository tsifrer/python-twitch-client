Videos
======

.. currentmodule:: twitch.api.videos

.. class:: Videos()

    This class provides methods for easy access to `Twitch Videos API`_.

    .. classmethod:: get_by_id(video_id)

        Gets a Video object based on specified video ID.

        :param string/int video_id: Video ID


    .. classmethod:: get_top(limit, offset, game, period, broadcast_type)

        Gets a list of top videos.

        :param int limit: Maximum number of objects to return. Default 10. Maximum 100.
        :param int offset: Object offset for pagination of result. Default 0.
        :param string game: Name of the game.
        :param string period: Window of time to search. Default PERIOD_WEEK.
        :param string broadcast_type: Type of broadcast returned. Default BROADCAST_TYPE_HIGHLIGHT.
        

    .. classmethod:: get_followed_videos(limit, offset, broadcast_type)

        Gets a list of followed videos based on a specified OAuth token.

        :param int limit: Maximum number of objects to return. Default 10. Maximum 100.
        :param int offset: Object offset for pagination of result. Default 0.
        :param string broadcast_type: Type of broadcast returned. Default BROADCAST_TYPE_HIGHLIGHT.


        .. code-block:: python

            >>> from twitch import TwitchClient
            >>> client = TwitchClient('<my client id>', '<my oauth token>')
            >>> videos = client.videos.get_followed_videos()



.. _`Twitch Videos API`: https://dev.twitch.tv/docs/v5/reference/videos/
