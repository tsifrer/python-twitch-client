Clips
====

.. currentmodule:: twitch.api.clips

.. class:: Clips()

    This class provides methods for easy access to `Twitch Clips API`_.

    .. classmethod:: get_by_slug(slug)

        Gets a clip object based on the slug provided

        :param string slug: Twitch Slug.


    .. classmethod:: get_top(channel, cursor, game, language, limit, period, trending)

        Gets all clips emoticons in one or more specified sets.

        :param string channel: Channel name. If this is specified, top clips for only this channel are returned; otherwise, top clips for all channels are returned. If both channel and game are specified, game is ignored.
        :param string cursor: Tells the server where to start fetching the next set of results, in a multi-page response.
        :param string game: Game name. (Game names can be retrieved with the Search Games endpoint.) If this is specified, top clips for only this game are returned; otherwise, top clips for all games are returned. If both channel and game are specified, game is ignored.
        :param string language: Comma-separated list of languages, which constrains the languages of videos returned. Examples: es, en,es,th. If no language is specified, all languages are returned.
        :param int limit: Maximum number of most-recent objects to return. Default: 10. Maximum: 100.
        :param string period: The window of time to search for clips. Valid values: day, week, month, all. Default: week.
        :param boolean trending: If True, the clips returned are ordered by popularity; otherwise, by viewcount. Default: False.


    .. classmethod:: get_followed()

        Gets top clips for games followed by the user identified by OAuth token. Results are ordered by popularity.


.. _`Twitch Clips API`: https://dev.twitch.tv/docs/v5/reference/clips
