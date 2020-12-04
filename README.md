python-twitch-client
====================

[![Latest docs][docs-img]][docs]
[![Latest version][pypi-img]][pypi]
[![Latest build][ci-img]][gh-actions]
[![Coverage][codecov-img]][codecov]




`python-twitch-client` is an easy to use Python library for accessing the
Twitch API

You can find more information in the [documentation][docs] or for support, you can join the [Discord Server](https://discord.me/twitch-api).


Note
==============================================

`python-twitch-client` currently supports Twitch API v5 and the new Helix API.

If you find a missing endpoint or a bug please raise an [issue][issues] or
contribute and open a [pull request][pulls].


Basic Usage
==============================================
Helix API

```python
from itertools import islice
from twitch import TwitchHelix

client = TwitchHelix(client_id='<my client id>')
streams_iterator = client.get_streams(page_size=100)
for stream in islice(streams_iterator, 0, 500):
    print(stream)
```


Twitch API v5
```python
from twitch import TwitchClient

client = TwitchClient(client_id='<my client id>')
channel = client.channels.get_by_id(44322889)

print(channel.id)
print(channel.name)
print(channel.display_name)
```

[docs]: http://python-twitch-client.rtfd.io
[docs-img]: https://readthedocs.org/projects/python-twitch-client/badge/?version=latest (Latest docs)
[pulls]: https://github.com/tsifrer/python-twitch-client/pulls
[issues]: https://github.com/tsifrer/python-twitch-client/issues
[pypi]: https://pypi.python.org/pypi/python-twitch-client/
[pypi-img]: https://img.shields.io/pypi/v/python-twitch-client.svg
[codecov]: https://codecov.io/gh/tsifrer/python-twitch-client
[codecov-img]: https://codecov.io/gh/tsifrer/python-twitch-client/branch/master/graph/badge.svg
[gh-actions]: https://github.com/tsifrer/python-twitch-client/actions
[ci-img]: https://github.com/tsifrer/python-twitch-client/workflows/CI/badge.svg
