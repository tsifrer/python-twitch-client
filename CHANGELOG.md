# Changelog

## master


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
