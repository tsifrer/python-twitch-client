python-twitch-client
====================

[![Latest docs][docs-img]][docs]
[![Latest version][pypi-img]][pypi]


`python-twitch-client` is an easy to use Python library for accessing the
Twitch API

You can find more information in the [documentation][docs].


Note
==============================================

`python-twitch-client` currently supports Twitch API v5.

Not all endpoints are currently implemented.

If you want one implemented please raise an [issue][issues] or contribute and open pa [pull request][pulls].


Basic Usage
==============================================

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
