from twitch.api.base import TwitchAPI
from twitch.decorators import oauth_required
from twitch.exceptions import TwitchAttributeException
from twitch.resources import Comment, Post


class ChannelFeed(TwitchAPI):

    def get_posts(self, channel_id, limit=10, cursor=None, comments=5):
        if limit > 100:
            raise TwitchAttributeException(
                'Maximum number of objects returned in one request is 100')
        if comments > 5:
            raise TwitchAttributeException(
                'Maximum number of comments returned in one request is 5')

        params = {
            'limit': limit,
            'cursor': cursor,
            'comments': comments
        }
        response = self._request_get('feed/{}/posts'.format(channel_id), params=params)
        return [Post.construct_from(x) for x in response['posts']]

    def get_post(self, channel_id, post_id, comments=5):
        if comments > 5:
            raise TwitchAttributeException(
                'Maximum number of comments returned in one request is 5')

        params = {
            'comments': comments
        }
        response = self._request_get('feed/{}/posts/{}'.format(channel_id, post_id), params=params)
        return Post.construct_from(response)

    @oauth_required
    def create_post(self, channel_id, content, share=None):
        data = {
            'content': content
        }
        params = {
            'share': share
        }
        response = self._request_post('feed/{}/posts'.format(channel_id), data, params=params)
        return Post.construct_from(response['post'])

    @oauth_required
    def delete_post(self, channel_id, post_id):
        response = self._request_delete('feed/{}/posts/{}'.format(channel_id, post_id))
        return Post.construct_from(response)

    @oauth_required
    def create_reaction_to_post(self, channel_id, post_id, emote_id):
        params = {
            'emote_id': emote_id
        }
        url = 'feed/{}/posts/{}/reactions'.format(channel_id, post_id)
        response = self._request_post(url, params=params)
        return response

    @oauth_required
    def delete_reaction_to_post(self, channel_id, post_id, emote_id):
        params = {
            'emote_id': emote_id
        }
        url = 'feed/{}/posts/{}/reactions'.format(channel_id, post_id)
        response = self._request_delete(url, params=params)
        return response

    def get_post_comments(self, channel_id, post_id, limit=10, cursor=None):
        if limit > 100:
            raise TwitchAttributeException(
                'Maximum number of objects returned in one request is 100')

        params = {
            'limit': limit,
            'cursor': cursor,
        }
        url = 'feed/{}/posts/{}/comments'.format(channel_id, post_id)
        response = self._request_get(url, params=params)
        return [Comment.construct_from(x) for x in response['comments']]

    @oauth_required
    def create_post_comment(self, channel_id, post_id, content):
        data = {
            'content': content
        }
        url = 'feed/{}/posts/{}/comments'.format(channel_id, post_id)
        response = self._request_post(url, data)
        return Comment.construct_from(response)

    @oauth_required
    def delete_post_comment(self, channel_id, post_id, comment_id):
        url = 'feed/{}/posts/{}/comments/{}'.format(channel_id, post_id, comment_id)
        response = self._request_delete(url)
        return Comment.construct_from(response)

    @oauth_required
    def create_reaction_to_comment(self, channel_id, post_id, comment_id, emote_id):
        params = {
            'emote_id': emote_id
        }
        url = 'feed/{}/posts/{}/comments/{}/reactions'.format(channel_id, post_id, comment_id)
        response = self._request_post(url, params=params)
        return response

    @oauth_required
    def delete_reaction_to_comment(self, channel_id, post_id, comment_id, emote_id):
        params = {
            'emote_id': emote_id
        }
        url = 'feed/{}/posts/{}/comments/{}/reactions'.format(channel_id, post_id, comment_id)
        response = self._request_delete(url, params=params)
        return response
