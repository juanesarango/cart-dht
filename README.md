# Shopping Cart Service 🛒

The following service uses an implementation of an API using a sharded Ditributed Hash Table (DHT) in the backend.

## Content of the files

- The `store.py` has defined classes for the data backend:

  - `DHTServer`: each of the instances storing the customer's shopping carts as key-value pairs.
  - `DHTServerStore`: the array of DHTServes, that distrubutes the i/o data across the shards.

- The `api.py` the methods of the shopping cart to read/write the info into the sharded DHT, and has the main endpoint methods to respond to user interactions:

| Endpoint                      |  Method  |                          Body Data                           |           Description           |
| :---------------------------- | :------: | :----------------------------------------------------------: | :-----------------------------: |
| `/items/<customerId>`         |  `GET`   |                                                              |    List shopping Cart items     |
| `/item/<customerId>/<itemId>` |  `POST`  | `offeredPrice`, `itemCount`, `specialSale`, `saleExpiration` |     Add Item to Cart (Buy)      |
| `/item/<customerId>/<itemId>` |  `PUT`   |                          `newCount`                          |        Update item count        |
| `/item/<customerId>/<itemId>` | `DELETE` |                              ``                              |      Delete Item from Cart      |
| `/items/<customerId>`         | `DELETE` |                              ``                              | Delete Customer Cart (Checkout) |

- The `utils.py` have useful methods to hash, serialize and parse date objects. These operations are done before storing the data in the DHT. The DHT validates that the key is a 64-bit integer and that the value is a bytearray.

  - `hash_key()`: encodes the input string to byte, hashes with SHA1, outputs a HEX which in converted to base 10 and only takes module 2^63 to ensure hashed key it's a 64-bit integer.

  - `serialize_value()`: converts the input python object as json string, encodes to byte and outputs a byte array.

  - `deserialize_value()`: converts the input byte array back to a json string that can be loaded again as python object.

- The `tests/test_api.py`: contains tests with mockup data to test the main api methods, checking that items and cart are properly updated for each api method as expected.

## Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Run the api server
export FLASK_APP=api.py
export FLASK_ENV=development
flask run
```

## Run Tests

```bash
pytest tests
```

## Explanation
