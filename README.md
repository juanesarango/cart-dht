# Shopping Cart Service

The folllowing service uses an implementation of an API using a sharded Ditributed Hash Table (DHT) in the backend.

## Content

- The `store.py` has defined classes for the data backend:

  - `DHTServer`: each of the instances storing the customer's shopping carts as key-value pairs.
  - `DHTServerStore`: the array of DHTServes, that distrubutes the i/o data across the shards.

- The `api.py` has the main endpoint methods to respond to user interactions.

TODO: Endpoints table

- The `utils.py` have useful methods to hash, serialize and parse date objects.

## Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Run the api server
export FLASK_APP=api.py
flask run
```

## Run Tests
