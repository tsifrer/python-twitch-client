from itertools import islice

from twitch import TwitchHelix


def clips():
    client = TwitchHelix()
    clip = client.get_clips(clip_ids=['AwkwardHelplessSalamanderSwiftRage'])
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


def streams_metadata():
    client = TwitchHelix()
    streams_metadata_iterator = client.get_streams_metadata()
    for metadata in islice(streams_metadata_iterator, 0, 10):
        print(metadata)


def user_follows():
    client = TwitchHelix()
    user_follows_iterator = client.get_user_follows(to_id=23161357)
    print('Total: {}'.format(user_follows_iterator.total))
    for user_follow in islice(user_follows_iterator, 0, 10):
        print(user_follow)
