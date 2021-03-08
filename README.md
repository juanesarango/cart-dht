# Shopping Cart Service 🛒

The following service uses an implementation of an API using a sharded Ditributed Hash Table (DHT) in the backend.

## Content

- The `store.py` has defined classes for the data backend:

  - `DHTServer`: each of the instances storing the customer's shopping carts as key-value pairs.
  - `DHTServerStore`: the array of DHTServes, that distrubutes the i/o data across the shards.

- The `api.py` has the main endpoint methods to respond to user interactions.

| Endpoint                      |  Method  |                          Body Data                           |           Description           |
| :---------------------------- | :------: | :----------------------------------------------------------: | :-----------------------------: |
| `/items/<customerId>`         |  `GET`   |                                                              |    List shopping Cart items     |
| `/item/<customerId>/<itemId>` |  `POST`  | `offeredPrice`, `itemCount`, `specialSale`, `saleExpiration` |     Add Item to Cart (Buy)      |
| `/item/<customerId>/<itemId>` |  `PUT`   |                          `newCount`                          |        Update item count        |
| `/item/<customerId>/<itemId>` | `DELETE` |                              ``                              |      Delete Item from Cart      |
| `/items/<customerId>`         | `DELETE` |                              ``                              | Delete Customer Cart (Checkout) |

- The `utils.py` have useful methods to hash, serialize and parse date objects.

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
