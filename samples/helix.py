from itertools import islice

from twitch import TwitchHelix


def clip():
    client = TwitchHelix()
    clip = client.get_clip('AwkwardHelplessSalamanderSwiftRage')
    print(clip)


def games():
    client = TwitchHelix()
    games = client.get_games(game_ids=[493057], names=['World of Warcraft'])
    print(games)


def streams():
    client = TwitchHelix()
    streams_iterator = client.get_streams()

    print(streams_iterator.next())


def first_500_streams():
    client = TwitchHelix()
    streams_iterator = client.get_streams(page_size=100)

    for stream in islice(streams_iterator, 0, 500):
        print(stream)


def top_games():
    client = TwitchHelix()
    games_iterator = client.get_top_games(page_size=3)
    for game in islice(games_iterator, 0, 6):
        print(game)


def videos():
    client = TwitchHelix()
    videos_iterator = client.get_videos(game_id=493057, page_size=5)
    for video in islice(videos_iterator, 0, 10):
        print(video)
