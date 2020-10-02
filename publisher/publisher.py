import os
import time

import pika
from pika import BlockingConnection
from pika.adapters.blocking_connection import BlockingChannel

HOST = os.environ.get("RABBIT_CONTAINER", "localhost")
EXCHANGE = os.environ.get("EXCHANGE", "basic_exchange")


def create_connection(host='localhost') -> BlockingConnection:
    return pika.BlockingConnection(
        pika.ConnectionParameters(host=host))


def create_channel(pika_connection: BlockingConnection) -> BlockingChannel:
    return pika_connection.channel()


if __name__ == '__main__':
    time.sleep(10)
    connection = create_connection(host=HOST)
    channel = create_channel(connection)
    channel.exchange_declare(exchange=EXCHANGE, exchange_type='fanout')
    data_dir = os.listdir(
            os.path.join(
                os.path.dirname(
                    os.path.abspath(__file__)), "..", "data")
        )
    for x in data_dir:
        with open(x, "rb") as message:
            channel.basic_publish(
                exchange=EXCHANGE,
                routing_key='',
                body=message
            )
    connection.close()
