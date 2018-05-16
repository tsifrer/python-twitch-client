# Changelog

## Master

- Removed support for Python 3.3


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
