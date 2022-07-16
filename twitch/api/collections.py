from twitch.api.base import TwitchAPI
from twitch.decorators import oauth_required
from twitch.exceptions import TwitchAttributeException
from twitch.resources import Collection, Item


class Collections(TwitchAPI):
    async def get_metadata(self, collection_id):
        response = await self._request_get("collections/{}".format(collection_id))
        return Collection.construct_from(response)

    async def get(self, collection_id, include_all_items=False):
        params = {"include_all_items": include_all_items}
        response = await self._request_get(
            "collections/{}/items".format(collection_id), params=params
        )
        return [Item.construct_from(x) for x in response["items"]]

    async def get_by_channel(self, channel_id, limit=10, cursor=None, containing_item=None):
        if limit > 100:
            raise TwitchAttributeException(
                "Maximum number of objects returned in one request is 100"
            )
        params = {
            "limit": limit,
            "cursor": cursor,
        }
        if containing_item:
            params["containing_item"] = containing_item
        response = await self._request_get("channels/{}/collections".format(channel_id))
        return [Collection.construct_from(x) for x in response["collections"]]

    @oauth_required
    async def create(self, channel_id, title):
        data = {
            "title": title,
        }
        response = await self._request_post(
            "channels/{}/collections".format(channel_id), data=data
        )
        return Collection.construct_from(response)

    @oauth_required
    async def update(self, collection_id, title):
        data = {
            "title": title,
        }
        await self._request_put("collections/{}".format(collection_id), data=data)

    @oauth_required
    async def create_thumbnail(self, collection_id, item_id):
        data = {
            "item_id": item_id,
        }
        await self._request_put("collections/{}/thumbnail".format(collection_id), data=data)

    @oauth_required
    async def delete(self, collection_id):
        await self._request_delete("collections/{}".format(collection_id))

    @oauth_required
    async def add_item(self, collection_id, item_id, item_type):
        data = {"id": item_id, "type": item_type}
        response = await self._request_put(
            "collections/{}/items".format(collection_id), data=data
        )
        return Item.construct_from(response)

    @oauth_required
    async def delete_item(self, collection_id, collection_item_id):
        url = "collections/{}/items/{}".format(collection_id, collection_item_id)
        await self._request_delete(url)

    @oauth_required
    async def move_item(self, collection_id, collection_item_id, position):
        data = {"position": position}
        url = "collections/{}/items/{}".format(collection_id, collection_item_id)
        await self._request_put(url, data=data)
