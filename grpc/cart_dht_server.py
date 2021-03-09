"""Client DHT making queries."""
from concurrent import futures
import logging

import grpc

import cart_pb2
import cart_pb2_grpc

from cart import utils
from cart.store import DHTServerStore

shopping_cart = DHTServerStore(5)

class Shopper(cart_pb2_grpc.ShopperServicer):

    def GetItem(self, request, context):
        value = shopping_cart.get_item(request.key)
        return cart_pb2.ItemReply(
            key=request.key,
            value=str(value)
        )

    def WriteItem(self, request, context):
        shopping_cart.put_item(request.key, request.value)
        return cart_pb2.ItemStatus(
            result="ok"
        )


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    cart_pb2_grpc.add_ShopperServicer_to_server(Shopper(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()


