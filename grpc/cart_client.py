"""Client API making queries to DHT."""
import logging
import grpc

import cart_pb2
import cart_pb2_grpc


def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = cart_pb2_grpc.ShopperStub(channel)
        response = stub.GetItem(cart_pb2.ItemRequest(key=3243))
        print(f"Value received: {response.key} - {response.value}")

if __name__ == '__main__':
    logging.basicConfig()
    run()
