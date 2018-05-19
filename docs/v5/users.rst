Users
=====

.. currentmodule:: twitch.api.users

.. class:: Users()

    This class provides methods for easy access to `Twitch Users API`_.

    .. classmethod:: get()

        Gets a user object based on the OAuth token provided.


    .. classmethod:: get_by_id(user_id)

        Gets a user object based on specified user id.

        :param 'string user_id: User ID


    .. classmethod:: get_emotes(user_id)

        Gets a list of the emojis and emoticons that the specified user can use in chat

        :param 'string user_id: User ID



    .. classmethod:: check_subscribed_to_channel(user_id, channel_id)

        Checks if a specified user is subscribed to a specified channel.

        :param 'string user_id: User ID
        :param 'string channel_id: ID of the channel you want to check if user is
                          subscribed to


    .. classmethod:: get_follows(user_id, limit, offset, direction, sort_by)

        Gets a list of all channels followed by a specified user.

        :param 'string user_id: User ID
        :param int limit: Maximum number of objects to return. Default 25. Maximum 100.
        :param int offset: Object offset for pagination of result. Default 0.
        :param string direction: Sorting direction. Default DIRECTION_DESC.
        :param string sort_by: Sorting key. Default USERS_SORT_BY_CREATED_AT.


    .. classmethod:: check_follows_channel(user_id, channel_id)

        Checks if a specified user follows a specified channel.

        :param 'string user_id: User ID
        :param 'string channel_id: ID of the channel you want to check if user is following


    .. classmethod:: follow_channel(user_id, channel_id, notifications)

        Adds a specified user to the followers of a specified channel.

        :param 'string user_id: User ID
        :param 'string channel_id: ID of the channel you want user to follow
        :param boolean notifications: If true, the user gets email or push notifications when the
                    channel goes live. Default False.


    .. classmethod:: unfollow_channel(user_id, channel_id)

        Deletes a specified user from the followers of a specified channel.

        :param 'string user_id: User ID
        :param 'string channel_id: ID of the channel you want user to unfollow


    .. classmethod:: get_user_block_list(user_id, limit, offset)

        Gets a user’s block list.

        :param 'string user_id: User ID
        :param int limit: Maximum number of objects to return. Default 25. Maximum 100.
        :param int offset: Object offset for pagination of result. Default 0.


    .. classmethod:: block_user(user_id, blocked_user_id)

        Blocks a user.

        :param 'string user_id: User ID
        :param 'string blocked_user_id: ID of the user you wish to block


    .. classmethod:: unblock_user(user_id, blocked_user_id)

        Unblocks a user.

        :param 'string user_id: User ID
        :param 'string blocked_user_id: ID of the user you wish to unblock


    .. classmethod:: translate_usernames_to_ids(usernames)

        Translates a list of usernames to user ID's.

        :param list[string] usernames: List of usernames you wish to get ID's of


        .. code-block:: python

            >>> from twitch import TwitchClient
            >>> client = TwitchClient('<my client id>')
            >>> users = client.users.translate_usernames_to_ids(['lirik', 'giantwaffle'])
            >>>
            >>> for user in users:
            >>>     print('{}: {}'.format(user.name, user.id))
            'lirik: 23161357'
            'giantwaffle: 22552479'



.. _`Twitch Users API`: https://dev.twitch.tv/docs/v5/reference/users/
