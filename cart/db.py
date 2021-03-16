"""Db Methods to Access the DTH backend"""
import os
import json
from dotenv import load_dotenv
from azure.cosmosdb.table import TableService, Entity
from azure.common import (
    AzureHttpError,
    AzureConflictHttpError,
    AzureMissingResourceHttpError,
)

from cart import utils
from cart.local_store import DHTServerStore

# Get Azure Credentials
load_dotenv()

CONNECTION_STRING = os.getenv("AZURE_COSMOS_CONNECTION_STRING")
if not CONNECTION_STRING:
    ACCOUNT_KEY = os.getenv("AZURE_COSMOS_ACCOUNT_KEY")
    ACCOUNT_NAME = os.getenv("AZURE_COSMOS_ACCOUNT_NAME")
    TABLE_ENDPOINT = os.getenv("AZURE_COSMOS_TABLE_ENDPOINT")
    CONNECTION_STRING = (
        f"DefaultEndpointsProtocol=https;"
        f"AccountName={ACCOUNT_NAME};"
        f"AccountKey={ACCOUNT_KEY};"
        f"TableEndpoint={TABLE_ENDPOINT};"
    )

class ShoppingCartServiceCloud:
    """Shopping Cart Methods called from the API to interact with the DB."""

    def __init__(self, shards=1):
        self.shards = shards
        self.table_name = "ShoppingCartTable"
        self.db = TableService(
            endpoint_suffix="table.cosmos.azure.com",
            connection_string=CONNECTION_STRING,
        )
        try:
            self.db.create_table(self.table_name, fail_on_exist=True)
        except AzureConflictHttpError:
            # Accept error only if already exists
            pass

    def get_product_items(self, customer_id):
        row_key = utils.hash_key(customer_id)
        partition_key = 'ShoppingCart' + str(row_key % self.shards).zfill(3)

        # Get Entity
        try:
            items = self.db.get_entity(self.table_name, partition_key, str(row_key))
            product_items = json.loads(items.ProductItems)
        except AzureMissingResourceHttpError:
            product_items = []
        return product_items

    def update_product_items(self, customer_id, product_items):
        row_key = utils.hash_key(customer_id)
        partition_key = 'ShoppingCart' + str(row_key % self.shards).zfill(3)
        product_items = [item for item in product_items if item["unitCount"] > 0]

        # Insert or Update Items
        items = Entity()
        items.PartitionKey = partition_key
        items.RowKey = str(row_key)
        items.CustomerId = customer_id
        items.ProductItems = json.dumps(product_items)

        self.db.insert_or_replace_entity(self.table_name, items)

    def delete_shopping_cart(self, customer_id):
        row_key = utils.hash_key(customer_id)
        partition_key = 'ShoppingCart' + str(row_key % self.shards).zfill(3)

        # Get Items to Checkout before Delete
        try:
            items = self.db.get_entity(self.table_name, partition_key, str(row_key))
            checkout_items = json.loads(items.ProductItems)
        except AzureMissingResourceHttpError:
            checkout_items = []

        self.db.delete_entity(self.table_name, partition_key, str(row_key))
        return checkout_items


class ShoppingCartServiceLocal:
    """Shopping Cart Methods called from the API to interact with the DB."""

    def __init__(self, shards=1):
        self.db = DHTServerStore(shards)

    def get_product_items(self, customer_id):
        key = utils.hash_key(customer_id)
        value = self.db.get_item(key)
        return utils.deserialize_value(value)

    def update_product_items(self, customer_id, product_items):
        product_items = [item for item in product_items if item["unitCount"] > 0]
        key = utils.hash_key(customer_id)
        value = utils.serialize_value(product_items)
        self.db.put_item(key, value)

    def delete_shopping_cart(self, customer_id):
        key = utils.hash_key(customer_id)
        value = self.db.get_item(key)
        checkout_items = utils.deserialize_value(value)
        self.db.put_item(key, None)
        return checkout_items
