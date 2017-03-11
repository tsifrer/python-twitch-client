Chat
====

.. currentmodule:: twitch.api.chat

.. class:: Chat()

    This class provides methods for easy access to `Twitch Chat API`_.

    .. classmethod:: get_badges_by_channel(channel_id)

        Gets a list of badges that can be used in chat for a specified channel.

        :param string/int channel_id: Channel ID.


    .. classmethod:: get_emoticons_by_set(emotesets)

        Gets all chat emoticons in one or more specified sets.

        :param list emotesets: List of emoticon sets to be returned.


    .. classmethod:: get_all_emoticons()

        Gets all chat emoticons.


        .. code-block:: python

            >>> from twitch import TwitchClient
            >>> client = TwitchClient('<my client id>')
            >>> emotes = client.chat.get_all_emoticons()



.. _`Twitch Chat API`: https://dev.twitch.tv/docs/v5/reference/chat/
