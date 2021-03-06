import os
import pytest
from cart.api import app


def test_api():
    with app.test_client() as client:

        username = "jea265"
        upc_1 = "036000291459"
        upc_2 = "987243752377"

        checkout = False # flag to clean cart at the end

        # Initialize Empty Cart
        client.delete(f"/items/{username}")
        rv = client.get(f"/items/{username}")
        items = rv.get_json()
        assert not items and items == [], f"Cart should be empty: {items}"
        print("\nā 1/5: Cart is Empty")

        # Add items to cart
        client.post(
            f"/items/{username}/{upc_1}",
            json={
                "unitCount": 2,
                "offeredPrice": 50,
            },
        )
        client.post(
            f"/items/{username}/{upc_2}",
            json={
                "unitCount": 3,
                "offeredPrice": 10,
            },
        )
        rv = client.get(f"/items/{username}")
        items = rv.get_json()
        assert len(items) == 2, "Cart should have 2 products"
        assert items[0]["itemId"] == int(upc_1), "UPC not correct"
        assert items[0]["unitCount"] == 2, "Count is not correct"
        assert items[0]["offeredPrice"] == 50, "Price is not correct"
        assert items[1]["itemId"] == int(upc_2), "UPC not correct"
        assert items[1]["unitCount"] == 3, "Count is not correct"
        assert items[1]["offeredPrice"] == 10, "Price is not correct"
        print("ā 2/5: Cart with 2 Products")

        # Update item count
        client.put(
            f"/items/{username}/{upc_1}",
            json={
                "newCount": 1,
            },
        )
        rv = client.get(f"/items/{username}")
        items = rv.get_json()
        assert len(items) == 2, "Cart should have 2 products"
        assert items[0]["unitCount"] == 1, "Count is not correct"
        assert items[0]["offeredPrice"] == 50, "Price is not correct"
        print("ā 3/5: Product count updated")

        # Delete item from cart
        client.delete(f"/items/{username}/{upc_1}")
        rv = client.get(f"/items/{username}")
        items = rv.get_json()
        assert len(items) == 1, "Cart should have 1 product"
        assert items[0]["itemId"] == int(upc_2), "UPC not correct"
        assert items[0]["unitCount"] == 3, "Count is not correct"
        assert items[0]["offeredPrice"] == 10, "Price is not correct"
        print("ā 4/5: Removed one product from Cart")

        # Checkout
        if checkout:
            rv = client.post(f"/checkout/{username}")
            checkout_items = rv.get_json()
            assert (
                sum(item["unitCount"] * item["offeredPrice"] for item in checkout_items)
                == 30
            ), "Total Checkout should be 30."

            rv = client.get(f"/items/{username}")
            items = rv.get_json()
            assert not items and items == [], "Cart should be empty"
            print("ā 5/5: Checkout product cart and deleted")
        else:
            print("ā5/5: Not checking out to see test items online")
