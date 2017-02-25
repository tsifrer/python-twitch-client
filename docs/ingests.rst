Ingests
=============================

.. currentmodule:: twitch.api.ingests

.. class:: Ingests()

    This class provides methods for easy access to `Twitch Ingests API`_.

    .. classmethod:: get_server_list()

        Gets a list of ingest servers.

        .. code-block:: python

            >>> from twitch import TwitchClient
            >>> client = TwitchClient('<my client id>')
            >>> ingests = client.ingests.get_server_list()


.. _`Twitch Ingests API`: https://dev.twitch.tv/docs/v5/reference/ingests/
