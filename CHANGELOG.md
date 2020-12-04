# Changelog

## Master

- Moved test requirements to setup.py
- Updated dependencies to newer versions
- Removed support for Python 2, Python 3.4 and Python 3.5
- Added support for Python 3.7 and 3.8
- Added new code formatting called black
- Changed import orders to now be formatted via isort
- Added TwitchHelix.get_oauth() for fetching OAuth access token
- Updated docs

## Version 0.6.0 - 2018-09-10

- Added default request timeout to all requests for API v5
- Removed support for Python 3.3
- Added TwitchHelix class which adds support for the new Twitch Helix API.
- Added Twitch Helix API support for the following endpoints:
  * Get Clips `twitch.helix.api.TwitchHelix.get_clips`
  * Get Games `twitch.helix.api.TwitchHelix.get_games`
  * Get Streams `twitch.helix.api.TwitchHelix.get_streams`
  * Get Streams Metadata `twitch.helix.api.TwitchHelix.get_streams_metadata`
  * Get Top Games `twitch.helix.api.TwitchHelix.get_top_games`
  * Get User Follows `twitch.helix.api.TwitchHelix.get_user_follows`
  * Get Videos `twitch.helix.api.TwitchHelix.get_videos`
- Changed how config file is read and moved the corresponding code to twitch/conf.py
- Changed old string formatting to the new one


## Version 0.5.1 - 2018-03-03

- Fixed `configparser` import for Python<3.2


## Version 0.5.0 - 2018-02-06

- Added VOD download support


## Version 0.4.0 - 2017-11-17

- Added clips endpoints


## Version 0.3.1 - 2017-10-26

- Fixed Twitch.channels.get_subscribers function to obey filters
- Added support for `~/.twitch.cfg` file for storing credentials
- Added retry logic for all >=500 requests with a backoff functionality
- Added discord server to the docs
- Bumped up requirements: six from 1.10.0 to 1.11.0 and requests from 2.18.1 to 2.18.4


## Version 0.3.0 - 2017-06-01

- Fixed all post and put methods to pass data in json format to Twitch API rather than in form format
- Fixed Channels.update() method to correctly pass data to Twitch
- Fixed Channels.get() method to call 'channel' endpoint instead of 'channels'
- Fixed a bad implementation of _DateTime resource
- Added Streams.get_streams_in_community endpoint
- Added support for python 2.7
- Added six as a requirement


## Version 0.2.1 - 2017-5-2

- Fixed Streams.get_stream_by_user which raised exception if stream was offline. Now returns None
  if stream is offline.


## Version 0.2.0 - 2017-3-10

- Added pypi image to README.md
- Added CHANGELOG.md
- Added docs for `twitch.api.users`, `twitch.api.chat`, `twitch.api.communities`,
  `twitch.api.games`, `twitch.api.ingests`, `twitch.api.streams`, `twitch.api.teams`,
  `twitch.api.videos`
- Added Travis-CI
- Added Codecov
- Added a LOT of tests
- Added the rest of community endpoints
- Added loads of missing tests
- Added search endpoints
- Added channel feed endpoints
- Added collections endpoints
- Changed some function names for channels (will break stuff if you're using version 0.1.0 already)
- Fixed output from streams
- Fixed passing parameters to video endpoints
- Introduced TwitchException, TwitchAuthException and TwitchAttributeException
- `created_at` fields are now converted to datetime objects
- Removed 'create' method on communities endpoint


## Version 0.1.0 - 2017-2-25

Initial release
