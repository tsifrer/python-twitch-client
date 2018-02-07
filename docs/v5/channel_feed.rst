Channel feed
============

.. currentmodule:: twitch.api.channel_feed

.. class:: ChannelFeed()

    This class provides methods for easy access to `Twitch Channel Feed API`_.

    .. classmethod:: get_posts(channel_id, limit, cursor, comments)

        Gets posts from a specified channel feed.

        :param string channel_id: Channel ID
        :param int limit: Maximum number of objects to return. Default 10. Maximum 100.
        :param string cursor: Cursor of the next page
        :param int comments: Number of comments to return. Default 5. Maximum 5.


    .. classmethod:: get_post(channel_id, post_id, comments)

        Gets a specified post from a specified channel feed.

        :param string channel_id: Channel ID
        :param string post_id: Post ID
        :param int comments: Number of comments to return. Default 5. Maximum 5.

        .. code-block:: python

            >>> from twitch import TwitchClient
            >>> client = TwitchClient('<my client id>')
            >>> post = client.channel_feed.get_post('12345', '12345', comments=0)


    .. classmethod:: create_post(channel_id, content, share)

        Creates a post in a specified channel feed.

        :param string channel_id: Channel ID
        :param string content: Content of the post
        :param boolean share: When set to true, the post is shared on the channel’s Twitter feed.


    .. classmethod:: delete_post(channel_id, post_id)

        Deletes a specified post in a specified channel feed.

        :param string channel_id: Channel ID
        :param string post_id: Post ID


    .. classmethod:: create_reaction_to_post(channel_id, post_id, emote_id)

        Creates a reaction to a specified post in a specified channel feed.

        :param string channel_id: Channel ID
        :param string post_id: Post ID
        :param string emote_id: Emote ID


    .. classmethod:: delete_reaction_to_post(channel_id, post_id, emote_id)

        Deletes a specified reaction to a specified post in a specified channel feed.

        :param string channel_id: Channel ID
        :param string post_id: Post ID
        :param string emote_id: Emote ID


    .. classmethod:: get_post_comments(channel_id, post_id, limit, cursor)

        Gets all comments on a specified post in a specified channel feed.

        :param string channel_id: Channel ID
        :param string post_id: Post ID
        :param int limit: Maximum number of objects to return. Default 10. Maximum 100.
        :param string cursor: Cursor of the next page


    .. classmethod:: create_post_comment(channel_id, post_id, content)

        Creates a comment to a specified post in a specified channel feed.

        :param string channel_id: Channel ID
        :param string post_id: Post ID
        :param string content: Content of the comment


    .. classmethod:: delete_post_comment(channel_id, post_id, comment_id)

        Deletes a specified comment on a specified post in a specified channel feed.

        :param string channel_id: Channel ID
        :param string post_id: Post ID
        :param string comment_id: Comment ID
        

    .. classmethod:: create_reaction_to_comment(channel_id, post_id, comment_id, emote_id)

        Creates a reaction to a specified comment on a specified post in a specified channel feed.

        :param string channel_id: Channel ID
        :param string post_id: Post ID
        :param string comment_id: Comment ID
        :param string emote_id: Emote ID


    .. classmethod:: delete_reaction_to_comment(channel_id, post_id, comment_id, emote_id)

        Deletes a reaction to a specified comment on a specified post in a specified channel feed.

        :param string channel_id: Channel ID
        :param string post_id: Post ID
        :param string comment_id: Comment ID
        :param string emote_id: Emote ID


.. _`Twitch Channel Feed API`: https://dev.twitch.tv/docs/v5/reference/channel-feed/
