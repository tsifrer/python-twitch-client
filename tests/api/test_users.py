import json

import responses

from twitch.client import TwitchClient
from twitch.constants import BASE_URL
from twitch.resources import User


example_user_response = {
    '_id': '44322889',
    'bio': 'Just a gamer playing games and chatting. :)',
    'created_at': '2013-06-03T19:12:02.580593Z',
    'display_name': 'dallas',
    'logo': ('https://static-cdn.jtvnw.net/jtv_user_pictures/'
             'dallas-profile_image-1a2c906ee2c35f12-300x300.png'),
    'name': 'dallas',
    'type': 'staff',
    'updated_at': '2016-12-13T16:31:55.958584Z'
}


@responses.activate
def test_get_by_id():
    user_id = 1234
    responses.add(responses.GET,
                  '%susers/%s' % (BASE_URL, user_id),
                  body=json.dumps(example_user_response),
                  status=200,
                  content_type='application/json')

    client = TwitchClient('abcd')

    user = client.users.get_by_id(user_id)

    assert len(responses.calls) == 1
    assert isinstance(user, User)
    assert user.id == example_user_response['_id']
