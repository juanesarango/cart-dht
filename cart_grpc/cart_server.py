"""Client DHT making queries."""
from concurrent import futures
import logging

import grpc

import cart_pb2
import cart_pb2_grpc

# from cart import utils
# from cart.store import DHTServerStore

# shopping_cart = DHTServerStore(5)

class Shopper(cart_pb2_grpc.ShopperServicer):

    def GetItem(self, request, context):
        return cart_pb2.ItemReply(
            key=request.key,
            value='Juanchito'
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


