Channels
========

.. currentmodule:: twitch.api.channels

.. class:: Channels()

    This class provides methods for easy access to `Twitch Channels API`_.

    .. classmethod:: get()

        Gets a channel object based on the OAuth token.

        .. code-block:: python

            >>> from twitch import TwitchClient
            >>> client = TwitchClient('<my client id>', '<my oauth token>')
            >>> channel = client.channels.get()


    .. classmethod:: get_by_id(channel_id)

        Gets a specified channel object.

        :param string channel_id: Channel ID


    .. classmethod:: update(channel_id, status, game, delay, channel_feed_enabled)

        Updates specified properties of a specified channel.

        :param string channel_id: Channel ID
        :param string status: Description of the broadcaster’s status.
        :param string game: Name of game.
        :param int delay: Channel delay, in seconds.
        :param boolean channel_feed_enabled: If true, the channel’s feed is turned on.
        

    .. classmethod:: get_editors(channel_id)

        Gets a list of users who are editors for a specified channel.

        :param string channel_id: Channel ID


    .. classmethod:: get_followers(channel_id, limit, offset, cursor, direction)

        Gets a list of users who follow a specified channel.

        :param string channel_id: Channel ID
        :param int limit: Maximum number of objects to return. Default 25. Maximum 100.
        :param int offset: Object offset for pagination of result. Default 0.
        :param string cursor: Cursor of the next page.
        :param string direction: Direction of sorting.


    .. classmethod:: get_teams(channel_id)

        Gets a list of teams to which a specified channel belongs.

        :param string channel_id: Channel ID


    .. classmethod:: get_subscribers(channel_id, limit, offset, direction)

        Gets a list of users subscribed to a specified channel.

        :param string channel_id: Channel ID
        :param int limit: Maximum number of objects to return. Default 25. Maximum 100.
        :param int offset: Object offset for pagination of result. Default 0.
        :param string direction: Direction of sorting.


    .. classmethod:: check_subscription_by_user(channel_id, user_id)

        Checks if a specified channel has a specified user subscribed to it.

        :param string channel_id: Channel ID
        :param string user_id: User ID


    .. classmethod:: get_videos(channel_id, limit, offset, broadcast_type, language, sort)

        Gets a list of videos from a specified channel.

        :param string channel_id: Channel ID
        :param int limit: Maximum number of objects to return. Default 10. Maximum 100.
        :param int offset: Object offset for pagination of result. Default 0.
        :param string broadcast_type: Constrains the type of videos returned.
        :param string language: Constrains the language of the videos that are returned.
        :param string sort: Sorting order of the returned objects.


    .. classmethod:: start_commercial(channel_id, duration)

        Starts a commercial (advertisement) on a specified channel.

        :param string channel_id: Channel ID
        :param string duration: Duration of the commercial in seconds. Default 30.


    .. classmethod:: reset_stream_key(channel_id)

        Deletes the stream key for a specified channel. Stream key is automatically reset.

        :param string channel_id: Channel ID


    .. classmethod:: get_community(channel_id)

        Gets the community for a specified channel.

        :param string channel_id: Channel ID


    .. classmethod:: set_community(channel_id, community_id)

        Sets a specified channel to be in a specified community.

        :param string channel_id: Channel ID
        :param string community_id: Community ID


    .. classmethod:: delete_from_community(channel_id)

        Deletes a specified channel from its community.

        :param string channel_id: Channel ID



.. _`Twitch Channels API`: https://dev.twitch.tv/docs/v5/reference/channels/
