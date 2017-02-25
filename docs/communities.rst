Communities
=============================

.. currentmodule:: twitch.api.users

.. class:: Communities()

    This class provides methods for easy access to `Twitch Communities API`_.

    .. classmethod:: get_by_name(community_name)

        Gets a specified community.

        :param string community_name: Name of the community


    .. classmethod:: get_by_id(community_id)

        Gets a Community object based on specified user id.

        :param string/int community_id: Community ID


    .. classmethod:: create(name, summary, description, rules)

        Creates a community.

        :param string name: Community name.
        :param string summary: Short description of the community.
        :param string description: Long description of the community.
        :param string rules: Rules displayed when viewing a community page.


    .. classmethod:: update(community_id, summary, description, rules, email)

        Updates a community.

        :param string/int community_id: Community ID
        :param string summary: Short description of the community.
        :param string description: Long description of the community.
        :param string rules: Rules displayed when viewing a community page.
        :param string email: Email address of the community owner.


        .. code-block:: python

            >>> from twitch import TwitchClient
            >>> client = TwitchClient('<my client id>', '<my oauth token>')
            >>> community = client.communities.update(12345, 'foo', 'bar')



.. _`Twitch Communities API`: https://dev.twitch.tv/docs/v5/reference/communities/
