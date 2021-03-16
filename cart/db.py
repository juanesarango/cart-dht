"""Db Methods to Access the DTH backend"""
from cart import utils
from cart.store import DHTServerStore

class ShoppingCartService:
    """Shopping Cart Methods called from the API to interact with the DB."""

    def __init__(self, shards=1):
        self.cart = DHTServerStore(shards)

    def get_product_items(self, customer_id):
        key = utils.hash_key(customer_id)
        value = self.cart.get_item(key)
        return utils.deserialize_value(value)


    def update_product_items(self, customer_id, product_items):
        product_items = [item for item in product_items if item["unitCount"] > 0]
        key = utils.hash_key(customer_id)
        value = utils.serialize_value(product_items)
        self.cart.put_item(key, value)


    def delete_shopping_cart(self, customer_id):
        key = utils.hash_key(customer_id)
        value = self.cart.get_item(key)
        checkout_items = utils.deserialize_value(value)
        self.cart.put_item(key, None)
        return checkout_items
