"""A sharded Distributed Hash Table (DHT) implementation for a Shoping Cart service."""


class DHTServer:
    """Key-Value Data Structure."""

    def __init__(self):
        """Use the built-in dict as the hash table."""
        self.items = dict()

    def get_item(self, key):
        """Return tuple of (version, value) if key exists in dict."""
        self.validate_key(key)
        return self.items[key] if key in self.items else (None, None)

    def put_item(self, key, value, desired_version):
        """Update value from key only if version is correct. Delete if none."""
        self.validate_value(value)

        # Fail if version is drifted
        current_version, _ = self.get_item(key)
        if current_version and current_version >= desired_version:
            return -1

        # Update or Delete
        if value:
            self.items[key] = desired_version, value
        else:
            del self.items[key]

        return True

    def validate_key(self, key):
        """Check key is a 64-bit integer."""
        if key.isdigit() and not key.bit_length() < 64:
            raise TypeError(f"Key is not a 64-bit integer: {key}")

    def validate_value(self, value):
        """Check value is a byte-array."""
        if not isinstance(value, bytearray):
            raise TypeError(f"Value is not a byte array: {value}")


class DHTServerStore:
    """Array of n DHTServer objects, to store sharded versioned key-value pairs."""

    def __init__(self, size):
        """Construct a store of N shards of DHT Servers."""
        self.size = size
        self.store = {i: DHTServer() for i in range(size)}

    def get_item(self, key):
        """Return value from proper shard."""
        shard = self.store[key % self.size]
        _, value = shard.get_item(key)
        return value

    def put_item(self, key, value):
        """Update value in shard and bumping its version."""
        shard = self.store[key % self.size]
        version, value = shard.get_item(key)
        return self.store[key % self.size].put_item(key, value, version + 1)


if __name__ == "__main__":

    shopping_cart = DHTServerStore(5)

    shopping_item = {
        "customerId": "jea265",
        "itemId": "03600029145",
        "offeredPrice": 250,
        "unitCount": 2,
        "timestamp": "2021-03-08 01:50:57",
        "specialSale": True,
        "saleExpiration": "2021-03-31 11:59:59",
    }
