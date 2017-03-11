Collections
===========

.. currentmodule:: twitch.api.collections

.. class:: Collections()

    This class provides methods for easy access to `Twitch Collections API`_.

    .. classmethod:: get_metadata(collection_id)

        Gets summary information about a specified collection.

        :param string collection_id: Collection ID

        .. code-block:: python

            >>> from twitch import TwitchClient
            >>> client = TwitchClient('<my client id>')
            >>> collection = client.collections.get_metadata('12345')


    .. classmethod:: get(collection_id, include_all_items)

        Gets all items in a specified collection.

        :param string collection_id: Collection ID
        :param boolean include_all_items: If True, unwatchable VODs are included in the response.
               Default: false.


    .. classmethod:: get_by_channel(channel_id, limit, cursor, containig_item)

        Gets all collections owned by a specified channel.

        :param string channel_id: Channel ID
        :param int limit: Maximum number of objects to return. Default 10. Maximum 100.
        :param string cursor: Cursor of the next page
        :param string containig_item: Returns only collections containing the specified video.
               `Example: video:89917098.`


    .. classmethod:: create(channel_id, title)

        Creates a new collection owned by a specified channel.

        :param string channel_id: Channel ID
        :param string title: Collection title


    .. classmethod:: update(collection_id, title)

        Updates the title of a specified collection.

        :param string collection_id: Collection ID
        :param string title: Collection title


    .. classmethod:: create_thumbnail(collection_id, item_id)

        Adds the thumbnail of a specified collection item as the thumbnail for the specified
        collection.

        :param string collection_id: Collection ID
        :param string item_id: Item ID


    .. classmethod:: delete(collection_id)

        Deletes a specified collection.

        :param string collection_id: Collection ID


    .. classmethod:: add_item(collection_id, item_id, item_type)

        Adds a specified item to a specified collection.

        :param string collection_id: Collection ID
        :param string item_id: Item ID
        :param string item_type: Type of the item. Example: `video`.


    .. classmethod:: delete_item(collection_id, collection_item_id)

        Deletes a specified collection item from a specified collection.

        :param string collection_id: Collection ID
        :param string collection_item_id: Collection Item ID


    .. classmethod:: move_item(collection_id, collection_item_id, position)

        Deletes a specified collection item from a specified collection.

        :param string collection_id: Collection ID
        :param string collection_item_id: Collection Item ID
        :param int position: New item position



.. _`Twitch Collections API`: https://dev.twitch.tv/docs/v5/reference/collections/
