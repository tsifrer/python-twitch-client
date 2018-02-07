Twitch Helix
============

Helix is the latest version of Twitch API

.. currentmodule:: twitch.helix

.. class:: TwitchHelix()

    This class provides methods for easy access to `Twitch Helix API`_.

    .. classmethod:: get_clip(clip_id)

        Gets information about a specified clip.

        :param string clip_id: ID of the clip being queried
        :return: :class:`~twitch.resources.Clip`

        .. code-block:: python

            >>> from twitch import TwitchHelix
            >>> helix = TwitchHelix('<my client id>')
            >>> clip = helix.get_clip('AwkwardHelplessSalamanderSwiftRage')


    .. classmethod:: get_games(game_ids=None, names=None)

        Gets game information by game ID or name.

        :param list game_ids: List of Game IDs. At most 100 id values can be specified.
        :param list names: List of Game names. The name must be an exact match. For instance, "Pokemon" will not return a list of Pokemon games; instead, query the specific Pokemon game(s) in which you are interested. At most 100 name values can be specified.
        :return: :class:`~twitch.resources.Game`


    .. classmethod:: get_streams(after=None, before=None, community_ids=None, page_size=None, game_ids=None, languages=None, stream_type=None, user_ids=None, user_logins=None)

        Gets information about active streams. Streams are returned sorted by number of current viewers, in descending order. Across multiple pages of results, there may be duplicate or missing streams, as viewers join and leave streams.

        :param string after: Cursor for forward pagination: tells the server where to start fetching the next set of results, in a multi-page response.
        :param string before: Cursor for backward pagination: tells the server where to start fetching the next set of results, in a multi-page response.
        :param list community_ids: Returns streams in a specified community ID. You can specify up to 100 IDs.
        :param integer page_size: Number of objects returned in one call. Maximum: 100. Default: 20.
        :param list game_ids: Returns streams broadcasting a specified game ID. You can specify up to 100 IDs.
        :param list languages: Stream language. You can specify up to 100 languages
        :param string stream_type: Stream type: "all", "live", "vodcast". Default: "all".
        :param list user_ids: Returns streams broadcast by one or more specified user IDs. You can specify up to 100 IDs.
        :param list user_logins: Returns streams broadcast by one or more specified user login names. You can specify up to 100 names.
        :return: :class:`~twitch.resources.Stream`


    .. classmethod:: get_top_games(after=None, before=None, page_size=None)

        Gets games sorted by number of current viewers on Twitch, most popular first.

        :param string after: Cursor for forward pagination: tells the server where to start fetching the next set of results, in a multi-page response.
        :param string before: Cursor for backward pagination: tells the server where to start fetching the next set of results, in a multi-page response.
        :param integer page_size: Number of objects returned in one call. Maximum: 100. Default: 20.
        :return: :class:`~twitch.resources.Game`


    .. classmethod:: get_videos(video_ids=None, user_id=None, game_id=None, after=None, before=None, page_size=None, language=None, period=None, sort=None, video_type=None)

        Gets video information by video ID (one or more), user ID (one only), or game ID (one only).

        :param list video_ids: List of Video IDs. Limit: 100.
        :param string user_id: ID of the user who owns the video.
        :param int game_id: ID of the game the video is of.
        :param string after: Cursor for forward pagination: tells the server where to start fetching the next set of results, in a multi-page response.
        :param string before: Cursor for backward pagination: tells the server where to start fetching the next set of results, in a multi-page response.
        :param integer page_size: Number of objects returned in one call. Maximum: 100. Default: 20.
        :param string language: Language of the video being queried.
        :param string period: Period during which the video was created. Valid values: "all", "day", "month", and "week".
        :param string sort: Sort order of the videos. Valid values: "time", "trending", and "views".
        :param string type: Type of video. Valid values: "all", "upload", "archive", and "highlight".
        :return: :class:`~twitch.resources.Video`


.. _`Twitch Helix API`: https://dev.twitch.tv/docs/api/reference
