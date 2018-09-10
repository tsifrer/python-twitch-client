===========
Basic Usage
===========

The ``python-twitch-client`` allows you to easily access to Twitch API endpoints.

This package is a modular wrapper designed to make Twitch API calls simpler and easier for you to
use. Provided below are examples of how to interact with commonly used API endpoints, but this is by no means
a complete list.

--------

Getting a channel by ID
-----------------------

.. code-block:: python

    from twitch import TwitchClient

    client = TwitchClient(client_id='<my client id>')
    channel = client.channels.get_by_id(44322889)

    print(channel.id)
    print(channel.name)
    print(channel.display_name)
