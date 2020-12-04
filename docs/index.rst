
Welcome to ``python-twitch-client``
===================================

An easy to use Python library for accessing the Twitch API

.. warning::
    This documentation is a work in progress

.. note::
    ``python-twitch-client`` currently supports Helix API and Twitch API v5.

    Helix API integration is a work in progress and some endpoints might be missing.

    If you find a missing endpoint or a bug please raise an issue_ or contribute and open a
    `pull request`_.


Installation
============

You can install ``python-twitch-client`` with ``pip``:

.. code-block:: console

    $ pip install python-twitch-client


``python-twitch-client`` is currently only tested and confirmed working on Linux and Mac. If you're
on a Windows machine and getting any bugs, please open a bug and help us find a solution.


Authentication
==============

Before you can use Twitch API you need to get the client ID. To get one, you should follow the
steps on `Twitch Authentication page`_.

Some of the endpoints also require OAuth token. To get one for testing purposes, you can use the
free `tokengen tool`_ or use TwitchHelix's ``get_oauth`` method.

There are two ways to pass credentials into the TwitchClient. The first and easiest way is to
just pass the credentials as an argument:

.. code-block:: python

    client = TwitchClient(client_id='<my client id>', oauth_token='<my oauth token>')

Other option is to create a config file `~/.twitch.cfg` which is a text file formatted as .ini
configuration file.

An example of the config file might look like:

.. code-block:: none

    [Credentials]
    client_id = <my client id>
    oauth_token = <my oauth token>

.. note::
    You only need to provide ``oauth_token`` if you're calling endpoints that need it.

    If you call functions that require ``oauth_token`` and you did not provide it, functions will
    raise ``TwitchAuthException`` exception.


Contents:
---------

.. toctree::
    :maxdepth: 0

    basic_usage
    helix
    v5/index


.. _issue: https://github.com/tsifrer/python-twitch-client/issues
.. _`pull request`: https://github.com/tsifrer/python-twitch-client/pulls
.. _`tokengen tool`: https://twitchapps.com/tokengen/
.. _`Twitch Authentication page`: https://dev.twitch.tv/docs/v5/guides/authentication/
