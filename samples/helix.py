from twitch import TwitchHelix


def streams():
    client = TwitchHelix()
    clip = client.get_clip('AwkwardHelplessSalamanderSwiftRage')
    print(clip)


if __name__ == '__main__':
    streams()
