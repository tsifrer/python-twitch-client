import json

import responses

from twitch.client import TwitchClient
from twitch.constants import BASE_URL
from twitch.resources import Team


example_team_response = {
    '_id': 10,
    'name': 'staff',
}

example_all_response = {
   'teams': [example_team_response]
}


@responses.activate
def test_get():
    team_name = 'spongebob'
    responses.add(responses.GET,
                  '%steams/%s' % (BASE_URL, team_name),
                  body=json.dumps(example_team_response),
                  status=200,
                  content_type='application/json')

    client = TwitchClient('client id', 'oauth token')

    team = client.teams.get(team_name)

    assert len(responses.calls) == 1
    assert isinstance(team, Team)
    assert team.id == example_team_response['_id']
    assert team.name == example_team_response['name']


@responses.activate
def test_get_all():
    responses.add(responses.GET,
                  '%steams' % BASE_URL,
                  body=json.dumps(example_all_response),
                  status=200,
                  content_type='application/json')

    client = TwitchClient('client id')

    teams = client.teams.get_all()

    assert len(responses.calls) == 1
    assert len(teams) == 1
    team = teams[0]
    assert isinstance(team, Team)
    assert team.id == example_team_response['_id']
    assert team.name == example_team_response['name']
