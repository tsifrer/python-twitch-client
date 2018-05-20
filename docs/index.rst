
Welcome to ``python-twitch-client``
===================================

An easy to use Python library for accessing the Twitch API

.. warning::
    This documentation is a work in progress

.. note::
    ``python-twitch-client`` currently supports Twitch API v5.

    Helix API integration is a work in progress and some enpoints are already avalible in the master branch.
    If you'd like to use the Helix API, install this library directly from this repository master branch.

    If you find a missing endpoint or a bug please raise an issue_ or contribute and open a
    `pull request`_.


Installation
============

You can install ``python-twitch-client`` with ``pip``:

.. code-block:: console

    $ pip install python-twitch-client


Authentication
==============

Before you can use Twitch API you need to get the client ID. To get one, you should follow the
steps on `Twitch Authentication page`_.

Some of the endpoints also require OAuth token. To get one for testing purposes, you can use the
free `tokengen tool`_.

There are two ways to pass credentials into the TwitchClient. The first and easies way is to
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
    v5/index
    helix


.. _issue: https://github.com/tsifrer/python-twitch-client/issues
.. _`pull request`: https://github.com/tsifrer/python-twitch-client/pulls
.. _`tokengen tool`: https://twitchapps.com/tokengen/
.. _`Twitch Authentication page`: https://dev.twitch.tv/docs/v5/guides/authentication/
