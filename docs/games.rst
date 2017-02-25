Games
=============================

.. currentmodule:: twitch.api.games

.. class:: Games()

    This class provides methods for easy access to `Twitch Games API`_.

    .. classmethod:: get_top(limit, offset)

        Gets a list of games sorted by number of current viewers.

        :param int limit: Maximum number of objects to return. Default 25. Maximum 100.
        :param int offset: Object offset for pagination of result. Default 0.

        .. code-block:: python

            >>> from twitch import TwitchClient
            >>> client = TwitchClient('<my client id>')
            >>> games = client.games.get_top()


.. _`Twitch Games API`: https://dev.twitch.tv/docs/v5/reference/games/
