import hashlib
from hashlib import sha256


class Item:

    key = None
    value = None

    def __init__(self, *args, **kwargs):
        self.update_item(*args, **kwargs)

    def update_item(
        self,
        customer_id,
        item_id,
        offered_price,
        unit_count,
        is_special_sale,
        sale_expiration_date,
    ):

        values = {
            "customer_id": customer_id,
            "item_id": item_id,
            "offered_price": offered_price,
            "unit_count": unit_count,
            "is_special_sale": is_special_sale,
            "sale_expiration_date": sale_expiration_date,
        }
        self.key = self.hash(f"{customer_id}-{item_id}")
        self.values = self.serialize(values)

    def get_item(key):
        pass

    def hash(key, bits=64):
        return sha256(key.encode("utf-8")).hexdigest()[:bits]

    def serialize(valies):
        pass
