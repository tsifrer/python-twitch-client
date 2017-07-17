import os

import pytest

from twitch import TwitchClient


@pytest.mark.parametrize('prop', [
    ('channel_feed'),
    ('channels'),
    ('chat'),
    ('collections'),
    ('communities'),
    ('games'),
    ('ingests'),
    ('search'),
    ('streams'),
    ('teams'),
    ('users'),
    ('videos'),
])
def test_client_properties(prop):
    c = TwitchClient()
    assert getattr(c, '_{}'.format(prop)) is None
    assert getattr(c, '{}'.format(prop)) is not None
    assert getattr(c, '_{}'.format(prop)) is not None


def test_client_reads_credentials_from_file(monkeypatch):

    def mockreturn(path):
        return 'tests/api/dummy_credentials.cfg'

    monkeypatch.setattr(os.path, 'expanduser', mockreturn)

    c = TwitchClient()
    assert c._client_id == 'spongebob'
    assert c._oauth_token == 'squarepants'
