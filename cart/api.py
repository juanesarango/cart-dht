"""Main API shopping cart."""
import json
import os
from datetime import datetime
from dotenv import load_dotenv
from flask import Flask, jsonify, request

from cart import utils
from cart.db import ShoppingCartServiceLocal, ShoppingCartServiceCloud

load_dotenv()
if os.getenv("DB_TYPE") == "Azure":
    print("Connecting to Azure CosmosDb...")
    shopping_cart = ShoppingCartServiceCloud(5)
else:
    print("Creating Local DHT as db...")
    shopping_cart = ShoppingCartServiceLocal(5)

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "")
app.shopping_cart = shopping_cart

@app.route("/items/<string:customer_id>", methods=["GET"])
def list_items(customer_id):
    product_items = shopping_cart.get_product_items(customer_id)
    return jsonify(product_items)


@app.route("/items/<string:customer_id>/<int:item_id>", methods=["POST"])
def add_item_to_cart(customer_id, item_id):
    product_items = shopping_cart.get_product_items(customer_id)

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
    shopping_cart.update_product_items(customer_id, product_items)

    return jsonify(new_item)


@app.route("/items/<string:customer_id>/<int:item_id>", methods=["PUT"])
def update_item_count(customer_id, item_id):
    product_items = shopping_cart.get_product_items(customer_id)
    new_count = request.get_json()["newCount"]

    # if item exist already merge count
    updated_item = None
    for item in product_items:
        if item["itemId"] == item_id:
            item["unitCount"] = new_count
            updated_item = item

    shopping_cart.update_product_items(customer_id, product_items)
    return jsonify(updated_item)


@app.route("/items/<string:customer_id>/<int:item_id>", methods=["DELETE"])
def delete_item_from_cart(customer_id, item_id):
    product_items = shopping_cart.get_product_items(customer_id)
    product_items = [item for item in product_items if item["itemId"] != item_id]
    shopping_cart.update_product_items(customer_id, product_items)

    return jsonify({})


@app.route("/items/<string:customer_id>", methods=["DELETE"])
def delete_cart(customer_id):
    shopping_cart.delete_shopping_cart(customer_id)
    return jsonify({})


@app.route("/checkout/<string:customer_id>", methods=["POST"])
def checkout_cart(customer_id):
    checkout_items = shopping_cart.delete_shopping_cart(customer_id)
    return jsonify(checkout_items)


if __name__ == "__main__":
    app.run(debug=True)
