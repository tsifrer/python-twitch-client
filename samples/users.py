from twitch import TwitchClient

CLIENT_ID = '<your client ID here>'


def translate_usernames_to_ids():
    client = TwitchClient(CLIENT_ID)
    users = client.users.translate_usernames_to_ids(['lirik', 'giantwaffle'])

    for user in users:
        print('{}: {}'.format(user.name, user.id))


if __name__ == '__main__':
    translate_usernames_to_ids()
