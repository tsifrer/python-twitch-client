Teams
=============================

.. currentmodule:: twitch.api.teams

.. class:: Teams()

    This class provides methods for easy access to `Twitch Teams API`_.

    .. classmethod:: get(team_name)

        Gets a specified team object.

        :param string team_name: Name of the team you want to get information of


    .. classmethod:: get_all(limit, offset)

        Gets all active teams.

        :param int limit: Maximum number of objects to return. Default 25. Maximum 100.
        :param int offset: Object offset for pagination of result. Default 0.


        .. code-block:: python

            >>> from twitch import TwitchClient
            >>> client = TwitchClient('<my client id>')
            >>> teams = client.teams.get_all()


.. _`Twitch Teams API`: https://dev.twitch.tv/docs/v5/reference/teams/
