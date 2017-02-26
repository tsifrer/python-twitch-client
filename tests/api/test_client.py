import pytest

from twitch import TwitchClient


@pytest.mark.parametrize('prop', [
    ('channels'),
    ('chat'),
    ('communities'),
    ('games'),
    ('ingests'),
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
