from twitch.api.base import TwitchAPI
from twitch.decorators import oauth_required
from twitch.exceptions import TwitchAttributeException
from twitch.resources import Collection, Item


class Collections(TwitchAPI):

    def get_metadata(self, collection_id):
        response = self._request_get('collections/%s' % collection_id)
        return Collection.construct_from(response)

    def get(self, collection_id, include_all_items=False):
        params = {
            'include_all_items': include_all_items
        }
        response = self._request_get('collections/%s/items' % collection_id, params=params)
        return [Item.construct_from(x) for x in response['items']]

    def get_by_channel(self, channel_id, limit=10, cursor=None, containing_item=None):
        if limit > 100:
            raise TwitchAttributeException(
                'Maximum number of objects returned in one request is 100')
        params = {
            'limit': limit,
            'cursor': cursor,
        }
        if containing_item:
            params['containing_item'] = containing_item
        response = self._request_get('channels/%s/collections' % channel_id)
        return [Collection.construct_from(x) for x in response['collections']]

    @oauth_required
    def create(self, channel_id, title):
        data = {
            'title': title,
        }
        response = self._request_post('channels/%s/collections' % channel_id, data=data)
        return Collection.construct_from(response)

    @oauth_required
    def update(self, collection_id, title):
        data = {
            'title': title,
        }
        self._request_put('collections/%s' % collection_id, data=data)

    @oauth_required
    def create_thumbnail(self, collection_id, item_id):
        data = {
            'item_id': item_id,
        }
        self._request_put('collections/%s/thumbnail' % collection_id, data=data)

    @oauth_required
    def delete(self, collection_id):
        self._request_delete('collections/%s' % collection_id)

    @oauth_required
    def add_item(self, collection_id, item_id, item_type):
        data = {
            'id': item_id,
            'type': item_type
        }
        response = self._request_put('collections/%s/items' % collection_id, data=data)
        return Item.construct_from(response)

    @oauth_required
    def delete_item(self, collection_id, collection_item_id):
        url = 'collections/%s/items/%s' % (collection_id, collection_item_id)
        self._request_delete(url)

    @oauth_required
    def move_item(self, collection_id, collection_item_id, position):
        data = {
            'position': position
        }
        url = 'collections/%s/items/%s' % (collection_id, collection_item_id)
        self._request_put(url, data=data)
