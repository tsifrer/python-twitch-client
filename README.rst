python-twitch-client
====================

.. image:: https://readthedocs.org/projects/python-twitch-client/badge/?version=latest
    :target: http://python-twitch-client.rtfd.io
    :alt: Latest Docs


``python-twitch-client`` is an easy to use Python library for accessing the
Twitch API


.. note::
    ``python-twitch-client`` currently supports Twitch API v5. 
    Not all endpoints are currently implemented.

    If you want one implemented please raise an issue_ or contribute and open pa `pull request`_.

You can find more information in the `documentation`_.


Basic Usage
==============================================

.. code-block:: python

    from twitch import TwitchClient

    client = TwitchClient(client_id='<my client id>')
    channel = client.channels.get_by_id(44322889)

    print(channel.id)
    print(channel.name)
    print(channel.display_name)


.. _`documentation`: http://python-twitch-client.rtfd.io
