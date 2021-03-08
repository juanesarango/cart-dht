"""Main API shopping cart."""
import json
from datetime import datetime

from flask import Flask, jsonify, request

import utils
from store import DHTServerStore

app = Flask(__name__)
app.secret_key = "cloud computing cs5412 - hw2"

shopping_cart = DHTServerStore(5)


# Shopping Cart Methods

def get_product_items(customer_id):
    key = utils.hash_key(customer_id)
    value = shopping_cart.get_item(key)
    return utils.deserialize_value(value)


def update_product_items(customer_id, product_items):
    product_items = [item for item in product_items if item["unitCount"] > 0]
    key = utils.hash_key(customer_id)
    value = utils.serialize_value(product_items)
    shopping_cart.put_item(key, value)


def delete_shopping_cart(customer_id):
    key = utils.hash_key(customer_id)
    value = shopping_cart.get_item(key)
    checkout_items = utils.deserialize_value(value)
    shopping_cart.put_item(key, None)
    return checkout_items


# Shopping Card Endpoints

@app.route("/items/<string:customer_id>", methods=["GET"])
def list_items(customer_id):
    product_items = get_product_items(customer_id)
    return jsonify(product_items)


@app.route("/items/<string:customer_id>/<int:item_id>", methods=["POST"])
def add_item_to_cart(customer_id, item_id):
    product_items = get_product_items(customer_id)

    new_item = request.get_json()
    new_item["itemId"] = item_id
    new_item["timestamp"] = utils.datetime_to_epoch(datetime.now())

    # default count 1 if not provided
    if not "unitCount" in new_item or not new_item["unitCount"]:
        new_item["unitCount"] = 1

    # if item exist already merge count
    has_item_already = new_item["itemId"] in [item["itemId"] for item in product_items]
    if has_item_already:
        current_unit_count = [
            item["unitCount"]
            for item in product_items
            if item["itemId"] == new_item["itemId"]
        ][0]
        new_item["unitCount"] += current_unit_count

    product_items.append(new_item)
    update_product_items(customer_id, product_items)

    return jsonify(new_item)


@app.route("/items/<string:customer_id>/<int:item_id>", methods=["PUT"])
def update_item_count(customer_id, item_id):
    product_items = get_product_items(customer_id)
    new_count = request.get_json()["newCount"]

    # if item exist already merge count
    updated_item = None
    for item in product_items:
        if item["itemId"] == item_id:
            item["unitCount"] = new_count
            updated_item = item

    update_product_items(customer_id, product_items)
    return jsonify(updated_item)


@app.route("/items/<string:customer_id>/<int:item_id>", methods=["DELETE"])
def delete_item_from_cart(customer_id, item_id):
    product_items = get_product_items(customer_id)
    product_items = [item for item in product_items if item["itemId"] != item_id]
    update_product_items(customer_id, product_items)

    return jsonify({})


@app.route("/items/<string:customer_id>", methods=["DELETE"])
def delete_cart(customer_id):
    delete_shopping_cart(customer_id)
    return jsonify({})

@app.route("/checkout/<string:customer_id>", methods=["POST"])
def checkout_cart(customer_id):
    checkout_items = delete_shopping_cart(customer_id)
    return jsonify(checkout_items)


if __name__ == "__main__":
    app.run(debug=True)
