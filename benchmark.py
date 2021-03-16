import datetime

from cart.api import app
from cart.db import ShoppingCartService


def parse_microseconds(dt):
    return int(dt.total_seconds() * 10 ** 6)


def run_several_times():
    import pandas as pd

    times = []
    for i in range(2):
        times.append(test_performance())

    df = pd.DataFrame(times)
    df.to_csv("times.tsv", sep="\t")


def test_performance():
    """Measure Cart Operations for several shard sizes."""
    times = {}
    for shard_number in [1, 10, 100, 1000, 10000]:

        app.shopping_cart = ShoppingCartService(shard_number)
        with app.test_client() as client:

            init_time = datetime.datetime.now()
            for i in range(100):
                username = "jea265"
                client.post(
                    f"/items/{username}/{str(i).zfill(12)}",
                    json={
                        "unitCount": 1,
                        "offeredPrice": 1,
                    },
                )
            add_items_time = datetime.datetime.now()
            checkout_items = client.post(f"/checkout/{username}").get_json()
            checkout_time = datetime.datetime.now()
            assert len(checkout_items) == 100, "Checkout Items were not 100"

            times[shard_number] = {
                "buying": parse_microseconds(add_items_time - init_time),
                "checkout": parse_microseconds(checkout_time - add_items_time),
                "total": parse_microseconds(checkout_time - init_time),
            }

    return times


if __name__ == "__main__":
    times = test_performance()

    # Print values
    print(f"N\tBuying\tCheckout\tTotal")
    for shard_number in [1, 10, 100, 1000, 10000]:
        a = times[shard_number]
        print(f"{shard_number}\t{a['buying']}\t{a['checkout']}\t\t{a['total']}")
