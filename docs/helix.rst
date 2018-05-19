Twitch Helix
============

Helix is the latest version of Twitch API

.. currentmodule:: twitch.helix

.. class:: TwitchHelix()

    This class provides methods for easy access to `Twitch Helix API`_.

    .. classmethod:: get_clips(clip_id)

        Gets clip information by clip ID (one or more), broadcaster ID (one only), or game ID (one only).

        :param string broadcaster_id: Broadcaster ID for whom clips are returned. The number of clips returned is determined by the ``page_size`` parameter (Default: 20 Max: 100). Results are ordered by view count.
        :param string game_id: Game ID for which clips are returned. The number of clips returned is determined by the ``page_size`` parameter (Default: 20 Max: 100). Results are ordered by view count.
        :param list clip_ids: List of clip IDS being queried. Limit: 100.
        :param string after (optional): Cursor for forward pagination: tells the server where to start fetching the next set of results, in a multi-page response.
        :param string before (optional): Cursor for backward pagination: tells the server where to start fetching the next set of results, in a multi-page response.
        :param integer page_size (optional): Number of objects returned in one call. Maximum: 100. Default: 20.
        :return: :class:`~twitch.helix.APICursor` if ``broadcaster_id`` or ``game_ids`` are provided, returns list of :class:`~twitch.resources.Clip` objects instead.

        For response fields of ``get_clips`` and official documentation check `Twitch Helix Get Clips`_.


    .. classmethod:: get_games(game_ids=None, names=None)

        Gets game information by game ID or name.

        :param list game_ids: List of Game IDs. At most 100 id values can be specified.
        :param list names: List of Game names. The name must be an exact match. For instance, "Pokemon" will not return a list of Pokemon games; instead, query the specific Pokemon game(s) in which you are interested. At most 100 name values can be specified.
        :return: :class:`~twitch.helix.APICursor` containing :class:`~twitch.resources.Game` objects

        For response fields of ``get_games`` and official documentation check `Twitch Helix Get Games`_.


    .. classmethod:: get_streams(after=None, before=None, community_ids=None, page_size=None, game_ids=None, languages=None, stream_type=None, user_ids=None, user_logins=None)

        Gets information about active streams. Streams are returned sorted by number of current viewers, in descending order. Across multiple pages of results, there may be duplicate or missing streams, as viewers join and leave streams.

        :param string after: Cursor for forward pagination: tells the server where to start fetching the next set of results, in a multi-page response.
        :param string before: Cursor for backward pagination: tells the server where to start fetching the next set of results, in a multi-page response.
        :param list community_ids: Returns streams in a specified community ID. You can specify up to 100 IDs.
        :param integer page_size: Number of objects returned in one call. Maximum: 100. Default: 20.
        :param list game_ids: Returns streams broadcasting a specified game ID. You can specify up to 100 IDs.
        :param list languages: Stream language. You can specify up to 100 languages
        :param list user_ids: Returns streams broadcast by one or more specified user IDs. You can specify up to 100 IDs.
        :param list user_logins: Returns streams broadcast by one or more specified user login names. You can specify up to 100 names.
        :return: :class:`~twitch.helix.APICursor` containing :class:`~twitch.resources.Stream` objects

        For response fields of ``get_streams`` and official documentation check `Twitch Helix Get Streams`_.


    .. classmethod:: get_top_games(after=None, before=None, page_size=None)

        Gets games sorted by number of current viewers on Twitch, most popular first.

        :param string after: Cursor for forward pagination: tells the server where to start fetching the next set of results, in a multi-page response.
        :param string before: Cursor for backward pagination: tells the server where to start fetching the next set of results, in a multi-page response.
        :param integer page_size: Number of objects returned in one call. Maximum: 100. Default: 20.
        :return: :class:`~twitch.helix.APICursor` containing :class:`~twitch.resources.Game` objects

        For response fields of ``get_top_games`` and official documentation check `Twitch Helix Get Top Games`_.


    .. classmethod:: get_videos(video_ids=None, user_id=None, game_id=None, after=None, before=None, page_size=None, language=None, period=None, sort=None, video_type=None)

        Gets video information by video ID (one or more), user ID (one only), or game ID (one only).

        :param list video_ids: List of Video IDs. Limit: 100.  If this is specified, you cannot use any of the optional query string parameters below.
        :param string user_id: User ID who owns the videos.
        :param int game_id: Game ID of the videos.
        :param string after (optional): Cursor for forward pagination: tells the server where to start fetching the next set of results, in a multi-page response.
        :param string before (optional): Cursor for backward pagination: tells the server where to start fetching the next set of results, in a multi-page response.
        :param integer page_size (optional): Number of objects returned in one call. Maximum: 100. Default: 20.
        :param string language (optional): Language of the video being queried.
        :param string period (optional): Period during which the video was created. Valid values: ``VIDEO_PERIODS``. Default: ``VIDEO_PERIOD_ALL``
        :param string sort (optional): Sort order of the videos. Valid values: ``VIDEO_SORTS``. Default: ``VIDEO_SORT_TIME``
        :param string type (optional): Type of video. Valid values: ``VIDEO_TYPES``. Default: ``VIDEO_TYPE_ALL``

        :return: :class:`~twitch.helix.APICursor` if ``user_id`` or ``game_id`` are provided, returns list of :class:`~twitch.resources.Video` objects instead.

        For response fields of ``get_videos`` and official documentation check `Twitch Helix Get Videos`_.


.. _`Twitch Helix API`: https://dev.twitch.tv/docs/api/reference
.. _`Twitch Helix Get Streams`: https://dev.twitch.tv/docs/api/reference/#get-streams
.. _`Twitch Helix Get Games`: https://dev.twitch.tv/docs/api/reference/#get-games
.. _`Twitch Helix Get Clips`: https://dev.twitch.tv/docs/api/reference/#get-clips
.. _`Twitch Helix Get Top Games`: https://dev.twitch.tv/docs/api/reference/#get-top-games
.. _`Twitch Helix Get Videos`: https://dev.twitch.tv/docs/api/reference/#get-videos
